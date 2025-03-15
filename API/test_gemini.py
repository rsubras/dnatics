from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
import base64, httpx
from dotenv import load_dotenv
import os

# Initialize the model

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=os.getenv("GOOGLE_API_KEY"))
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
# Download and encode the image
# Getting the base64 string
base64_image = encode_image(image_path)

# Create a message with the image
message = HumanMessage(
    content=[
        {"type": "text", "text": "describe the powerbi report in this image titled Medicine Sales Report"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        },
    ],
)

# Invoke the model with the message
response = model.invoke([message])

# Print the model's response
print(response.content)