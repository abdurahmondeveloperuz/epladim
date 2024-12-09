import json
import os
import tempfile
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from django.conf import settings

# Custom Exceptions
class StorageError(Exception):
    """Base exception for storage-related errors"""
    pass

class FileAccessError(StorageError):
    """Raised when there are problems accessing storage files"""
    pass

class DataCorruptionError(StorageError):
    """Raised when stored data is corrupted or invalid"""
    pass

# Data Models
@dataclass
class ClassData:
    class_id: str
    name: str

@dataclass
class StudentData:
    class_id: str
    first_name: str
    last_name: str
    score: float
    image: Optional[str] = ''
    profile_url: Optional[str] = '#'

class JSONStorage:
    def __init__(self):
        self.data_dir = os.path.join(settings.BASE_DIR, 'data')
        self.classes_file = os.path.join(self.data_dir, 'classes.json')
        self.students_file = os.path.join(self.data_dir, 'students.json')
        self._ensure_data_files()

    def _ensure_directory(self, directory_path: str) -> None:
        """Ensure directory exists with proper permissions"""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path, mode=0o755, exist_ok=True)

    def _atomic_write(self, file_path: str, data: Any) -> None:
        """Atomically write data to file"""
        directory = os.path.dirname(file_path)
        with tempfile.NamedTemporaryFile(mode='w', dir=directory, delete=False) as temp_file:
            json.dump(data, temp_file, indent=2)
            temp_file.flush()
            os.fsync(temp_file.fileno())
            os.chmod(temp_file.name, 0o666)
        
        try:
            os.replace(temp_file.name, file_path)
        except Exception as e:
            os.unlink(temp_file.name)
            raise RuntimeError(f"Failed to write file {file_path}: {str(e)}")

    def _ensure_data_files(self) -> None:
        """Ensure data directory and files exist with proper permissions"""
        try:
            self._ensure_directory(self.data_dir)
            
            for file_path in [self.classes_file, self.students_file]:
                if not os.path.exists(file_path):
                    self._atomic_write(file_path, [])
                os.chmod(file_path, 0o666)
        except Exception as e:
            raise FileAccessError(f"Failed to initialize data files: {str(e)}")

    def _load_data(self, file_path: str) -> List[Dict]:
        """Load data from JSON file with error handling"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self._ensure_data_files()
            return []
        except json.JSONDecodeError as e:
            backup_path = f"{file_path}.backup"
            os.rename(file_path, backup_path)
            self._ensure_data_files()
            raise DataCorruptionError(f"Data file corrupted, backup created at {backup_path}: {str(e)}")

    def _save_data(self, file_path: str, data: List[Dict]) -> None:
        """Save data to JSON file with error handling"""
        try:
            self._atomic_write(file_path, data)
        except Exception as e:
            raise FileAccessError(f"Failed to save data to {file_path}: {str(e)}")

    def get_class(self, class_id: str) -> Optional[Dict]:
        """Get class by ID"""
        classes = self._load_data(self.classes_file)
        return next((c for c in classes if c['class_id'] == class_id), None)

    def get_students(self, class_id: str) -> List[Dict]:
        """Get all students for a class"""
        students = self._load_data(self.students_file)
        return [s for s in students if s['class_id'] == class_id]

    def create_or_update_class(self, class_id: str, class_name: str, students_data: List[Dict]) -> int:
        """Create or update class and its students"""
        try:
            # Update class
            classes = self._load_data(self.classes_file)
            class_data = {'class_id': class_id, 'name': class_name}
            
            existing_class = next((i for i, c in enumerate(classes) if c['class_id'] == class_id), None)
            if existing_class is not None:
                classes[existing_class] = class_data
            else:
                classes.append(class_data)
            
            self._save_data(self.classes_file, classes)

            # Update students
            all_students = self._load_data(self.students_file)
            all_students = [s for s in all_students if s['class_id'] != class_id]
            
            new_students = []
            for student in students_data:
                new_student = {
                    'class_id': class_id,
                    'first_name': student['first_name'],
                    'last_name': student['last_name'],
                    'score': float(student['score']),
                    'image': student.get('image', ''),
                    'profile_url': student.get('profile_url', '#')
                }
                new_students.append(new_student)
            
            all_students.extend(new_students)
            self._save_data(self.students_file, all_students)

            return len(new_students)
        except Exception as e:
            raise FileAccessError(f"Failed to update class and students: {str(e)}")