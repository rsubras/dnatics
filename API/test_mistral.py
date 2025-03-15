import base64
import requests
import os
from dotenv import load_dotenv
from mistralai import Mistral

load_dotenv()

def encode_image(image_path):
    """Encode the image to base64."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: The file {image_path} was not found.")
        return None
    except Exception as e:  # Added general exception handling
        print(f"Error: {e}")
        return None

# Path to your image
# Path to your image
image_path = r"C:\Users\rsubr\Downloads\capture (16).png"  # Use raw string


# Getting the base64 string
base64_image = encode_image(image_path)

api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "image_url",
        "image_url": f"data:image/jpeg;base64,{base64_image}" 
    }
)


messages = [
  {
    "role": "user",
    "content": [
      {
        "type": "text",
        "text": "There is a PowerBI report in this image titled Medicine Sales Report, please analyze it and generate a narrative of the data displayed in 1000 words",
      },
      {
        "type": "text",
        "text": f"OCR Result: {ocr_response}",
      },
    ],
  }
]
chat_response = client.chat.complete(
  model="mistral-small-latest",
  messages=messages,
)

print(chat_response)