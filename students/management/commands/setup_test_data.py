from django.core.management.base import BaseCommand
from students.storage import JSONStorage
import base64
import os

class Command(BaseCommand):
    help = 'Creates initial test data'

    def handle(self, *args, **kwargs):
        storage = JSONStorage()
        
        # Test data
        class_id = 'TEST101'
        class_name = 'Test Class 101'
        
        # Default avatar image (you can replace this with your own default image)
        default_image = '''
        /9j/4AAQSkZJRgABAQEASABIAAD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wAARCABAAEADASIAAhEBAxEB/8QAGAABAQEBAQAAAAAAAAAAAAAAAAECAwT/xAAYEAEBAQEBAAAAAAAAAAAAAAAAAQIREv/EABQBAQAAAAAAAAAAAAAAAAAAAAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwD2YAAAAAAAAAAAAACiAoAAAAAAAAAAAAAAoigAAAAAAAAAAAAD/9k=
        '''
        
        students_data = [
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'score': 95.5,
                'image': default_image.strip()
            },
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'score': 98.0,
                'image': default_image.strip()
            },
            {
                'first_name': 'Bob',
                'last_name': 'Johnson',
                'score': 87.5,
                'image': default_image.strip()
            },
            {
                'first_name': 'Alice',
                'last_name': 'Brown',
                'score': 92.0,
                'image': default_image.strip()
            },
            {
                'first_name': 'Charlie',
                'last_name': 'Wilson',
                'score': 89.5,
                'image': default_image.strip()
            },
        ]

        # Save data
        storage.create_or_update_class(class_id, class_name, students_data)
        
        self.stdout.write(self.style.SUCCESS('Successfully created test data'))