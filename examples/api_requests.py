import requests
import json

# API Configuration
API_URL = "http://your-domain.com/api/set_class"  # Replace with your actual domain
API_KEY = "your-api-key-here"  # Replace with your API key
CLASS_ID = "TEST101"

# Sample data
class_data = {
    "class_name": "Python Programming 101",
    "students": [
        {
            "first_name": "John",
            "last_name": "Doe",
            "score": 95.5,
            "profile_url": "https://example.com/john-doe"
        },
        {
            "first_name": "Jane",
            "last_name": "Smith",
            "score": 98.0,
            "profile_url": "https://example.com/jane-smith"
        }
    ]
}

def send_class_data():
    """
    Send class data to the API using requests
    """
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Add class_id as query parameter
    url = f"{API_URL}?class_id={CLASS_ID}"
    
    try:
        response = requests.post(
            url,
            headers=headers,
            json=class_data
        )
        
        # Check if request was successful
        response.raise_for_status()
        
        # Print response
        print("Response Status:", response.status_code)
        print("Response Data:", response.json())
        
    except requests.exceptions.RequestException as e:
        print("Error occurred:", str(e))

# Using urllib (alternative method)
def send_class_data_urllib():
    """
    Send class data to the API using urllib
    """
    import urllib.request
    import urllib.error
    
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Add class_id as query parameter
    url = f"{API_URL}?class_id={CLASS_ID}"
    
    try:
        # Convert data to JSON string
        data = json.dumps(class_data).encode('utf-8')
        
        # Create request
        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method='POST'
        )
        
        # Send request
        with urllib.request.urlopen(req) as response:
            # Read and decode response
            response_data = response.read().decode('utf-8')
            print("Response Status:", response.status)
            print("Response Data:", json.loads(response_data))
            
    except urllib.error.URLError as e:
        print("Error occurred:", str(e))

# Example usage with error handling
def main():
    print("Sending request using requests library:")
    send_class_data()
    
    print("\nSending request using urllib:")
    send_class_data_urllib()

if __name__ == "__main__":
    main()