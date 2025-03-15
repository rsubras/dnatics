import base64
import requests
from PIL import Image
import json
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from typing import Dict
import os

# Import the necessary classes for Gemini model
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = FastAPI()
# Enable CORS
origins = [
    "http://localhost:3000",  # React app URL
    # Add other allowed origins here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = """Act as an OCR assistant. Analyze the provided image, it is a screen capture of a webpage and has a PowerBI report in it
1. Recognize all visuals in the PowerBI report and the associated data.
2. Provide relevant and accurate narration about what is illustrated in the powerbi report."""

def load_config():
    """Load the configuration file."""
    with open("config.json", "r") as config_file:
        return json.load(config_file)

config = load_config()
selected_model = config.get("model", "llama3.2-vision")

def encode_image_to_base64(image_path):
    """Convert an image file to a base64 encoded string."""
    print("Convert an image file to a base64 encoded string.")
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def perform_ocr(image_path) -> Dict[str, str]:
    """Perform OCR on the given image using the selected model."""
    print(f"Perform OCR on the given image using {selected_model}.")
    base64_image = encode_image_to_base64(image_path)
    
    if selected_model == "gemini-flash":
        print("Processing with Gemini")
        api_key = os.getenv("GOOGLE_API_KEY")
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=api_key)
        message = HumanMessage(
            content=[
                {"type": "text", "text": "describe the powerbi report in this image titled Medicine Sales Report"},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        )
        response = model.invoke([message])
        print("Response:", response.content)
        return {"content": response.content}
    else:
        print("PRocessing with Ollama ",selected_model)
        response = requests.post(
            "http://localhost:11434/api/chat",  # Ensure this URL matches your Ollama service endpoint
            json={
                "model": selected_model,
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
            print("Full response:", full_response)
            return {"content": full_response}
        else:
            print("Error:", response.status_code, response.text)
            return {"error": f"Error: {response.status_code} {response.text}"}

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
        result = perform_ocr(image_path)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)