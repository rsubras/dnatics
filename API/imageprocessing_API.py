import base64
import requests
from PIL import Image
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, JSONResponse
from dotenv import load_dotenv
from typing import AsyncGenerator
import os

load_dotenv()

app = FastAPI()

SYSTEM_PROMPT = """Act as an OCR assistant. Analyze the provided image, it is a screen capture of a webpage and has a PowerBI report in it
1. Recognize all visuals in the PowerBI report and the associated data.
2. Provide relevant and accurate narration about what is illustrated in the powerbi report."""

def encode_image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    print("Convert an image file to a base64 encoded string.")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

async def perform_ocr(image_path) -> AsyncGenerator[str, None]:
    """Perform OCR on the given image using Llama 3.2-Vision."""
    print("Perform OCR on the given image using Llama 3.2-Vision.")
    base64_image = encode_image_to_base64(image_path)
    response = requests.post(
        "http://localhost:11434/api/chat",  # Ensure this URL matches your Ollama service endpoint
        json={
            "model": "llama3.2-vision",
            "messages": [
                {
                    "role": "user",
                    "content": SYSTEM_PROMPT,
                    "images": [base64_image],
                },
            ],
        },
        stream=True
    )
    if response.status_code == 200:
        full_response = ""
        for line in response.iter_lines():
            if line:
                json_response = json.loads(line)
                content = json_response.get("message", {}).get("content", "")
                print("Current content:", content)
                yield content
    else:
        print("Error:", response.status_code, response.text)
        yield f"Error: {response.status_code} {response.text}"

        

@app.post("/ocr/")
async def ocr_endpoint(file: UploadFile = File(...)):
    """Endpoint to perform OCR on an uploaded image."""
    try:
        # Save the uploaded file
        image_path = f"temp_{file.filename}"
        with open(image_path, "wb") as image_file:
            content = await file.read()
            image_file.write(content)
        
        # Perform OCR
        print("Performing OCR on the uploaded image...")
        return StreamingResponse(perform_ocr(image_path), media_type="text/plain")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)