import asyncio
import aiohttp
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

async def send_class_data_async():
    """
    Send class data to the API using aiohttp (async)
    """
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Add class_id as query parameter
    url = f"{API_URL}?class_id={CLASS_ID}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, headers=headers, json=class_data) as response:
                print("Response Status:", response.status)
                response_data = await response.json()
                print("Response Data:", response_data)
                
        except aiohttp.ClientError as e:
            print("Error occurred:", str(e))

# Example usage with asyncio
async def main():
    print("Sending async request using aiohttp:")
    await send_class_data_async()

if __name__ == "__main__":
    asyncio.run(main())