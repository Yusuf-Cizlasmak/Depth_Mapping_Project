import os
from dotenv import load_dotenv
import requests
import base64

def get_api_key():
    load_dotenv()
    api_key = os.getenv("IMG_API_KEY")
    if api_key is None:
        raise Exception("API key not found in the .env file")
    return api_key

def upload_image(image_path):
    url = "https://api.imgbb.com/1/upload"
    try:
        with open(image_path, "rb") as file:
            image_data = base64.b64encode(file.read()).decode("utf-8")
            payload = {
                "key": get_api_key(),
                "image": image_data,
            }
            response = requests.post(url, data=payload)
            response.raise_for_status()
            result = response.json()
            return result
    except requests.exceptions.RequestException as e:
        return {"status": "Error", "error": str(e)}


def get_imgbb_result(image_path):
    try:
        api_key = get_api_key()
        result = upload_image(image_path, api_key)

        if result.get("status") == "success":
            return result
        else:
            print("Image upload failed.")
            if "error" in result and "message" in result["error"]:
                return f"Error Message: {result['error']['message']}"
            else:
                return "Error response structure not recognized."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
image_path = "path/to/your/image.jpg"
print(get_imgbb_result(image_path))
