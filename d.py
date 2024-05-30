import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image as PILImage

# Load environment variables
load_dotenv()

# Configure the generative AI model
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input_prompt, image):
    try:
        # Correct the model name as per Google's documentation
        model = genai.GenerativeModel("gemini-pro-vision")  # Ensure you replace with the correct model name
        response = model.generate_content([input_prompt, image[0]])
        return response.text
    except Exception as e:
        return str(e)

def input_image_setup(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()
        image_parts = [
            {
                "mime_type": upload_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit app
st.set_page_config(page_title="AI Food Analyzer")
st.header("AI Food Analyzer")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
display_image = None
if uploaded_file is not None:
    display_image = PILImage.open(uploaded_file)  # Use the alias for PIL Image
    st.image(display_image, caption="Uploaded image", use_column_width=True)

input_prompt = """
You are an expert nutritionist. Analyze dish name 
Neurients ratio in this food is as following:
1.Item 1 - Carbohydrates percentage
2.Item 2- Fats percentage
3.Item 3- Fibers percentage
4.Item 4-Sugar: percentage
5. Item 5- other percentage
Analyze the food items from the image and calculate the total calories. Also, provide the details of every food item with calorie intake in the following format:
1. Item 1 - number of calories
2. Item 2 - number of calories
...
And finally tell the food is healthy or not
Explain dish in details. 
....
...
"""

submit = st.button("Analyze Food")

if submit and uploaded_file is not None:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt, image_data)
    st.header("Food Analysis")
    st.write(response)
