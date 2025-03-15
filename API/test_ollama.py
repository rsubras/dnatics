import base64
import requests
from PIL import Image
import json

SYSTEM_PROMPT = """Act as an OCR assistant. Analyze the provided image, it is a screen capture of a webpage and has a PowerBI report in it
1. Recognize all visuals in the PowerBI report and the associated data.
2. Provide relevant and accurate narration about what is illustrated in the powerbi report."""
def encode_image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
def perform_ocr(image_path):
    """Perform OCR on the given image using Llama 3.2-Vision."""
    base64_image = encode_image_to_base64(image_path)
    response = requests.post(
        " http://localhost:11434/api/chat",  # Ensure this URL matches your Ollama service endpoint
        json={
            "model": "llama3.2-vision",
            "messages": [
                {
                    "role": "user",
                    "content": SYSTEM_PROMPT,
                    "images": [base64_image],
                },
            ],
        }
    )
    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
            content = json_response.get("message", {}).get("content", "")
            full_response += content
        return full_response
    else:
        print("Error:", response.status_code, response.text)
        return None
if __name__ == "__main__":
    image_path = r"C:\Users\rsubr\Downloads\capture (16).png"  # Replace with your image path
    result = perform_ocr(image_path)
    if result:
        print("OCR Recognition Result:")
        print(result)