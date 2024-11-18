import streamlit as st
import openai
import pandas as pd #this is for the excel
from PIL import Image
import os

sample_folder = "sample_images"

# List all image files in the folder
sample_images = [f for f in os.listdir(sample_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
# Function to load and display Excel data
def load_excel(file):
    df = pd.read_excel(file)
    df.columns = df.columns.str.strip()  # Clean up any extra spaces in column names
    st.write("Columns in the uploaded Excel file:", df.columns)
    return df
# Function to search for a user by name
def get_user_data(df, name):
    user_data = df[df['Name'] == name]
    return user_data

# Function to find a reference image from the sample folder based on user details
def get_reference_image(sample_images, user_data):
    # Logic to pick an image based on user preferences (e.g., location, favorite animal, etc.)
    # For simplicity, let's assume the user’s color or location is used to select an image
    user_color = user_data['Color'].values[0].lower()
    image_path = os.path.join(sample_images, f"{user_color}.jpg")  # Image named after color for example
    
    if os.path.exists(image_path):
        return Image.open(image_path)
    else:
        return None  # No match, return None

# Function to generate image using DALL-E with the prompt
def generate_image(user_data):
    #prompt=f"Generate an image of a cute cat with the Indian rupee symbol (₹) clearly and prominently displayed on its face. The image should be highly realistic and detailed. The rupee symbol should be well-defined and resemble the official currency symbol."
    prompt = f"The image generated should be for a {user_data['Age'].values[0]} year old {user_data['Color'].values[0]} person who likes {user_data['Food'].values[0]} and prefers {user_data['Place'].values[0]} setting. They also love animals, especially {user_data['Animal'].values[0]}Their favorite hobby is {user_data['Hobby'].values[0]},it should be suitable for digital printing."
  
    openai.api_key = openai.api_key = st.secrets["openai"]["api_key"]
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    
    image_url = response['data'][0]['url']
    return image_url

# Main Streamlit app
def main():
    st.title("User-Driven Image Generation with DALL-E and Sample Images")

    excel_file = st.file_uploader("Upload Excel file", type=["xlsx"])
    if excel_file:
        df = load_excel(excel_file)
        st.write("Uploaded Data:", df)

        user_name = st.text_input("Enter a user's name")
        
        if user_name:
            user_data = get_user_data(df, user_name)
            
            if not user_data.empty:
                st.write("User Data:", user_data)

                # Get the sample image from the sample folder
                sample_folder = 'sample_images'  # Folder containing reference images
                sample_image = get_reference_image(sample_folder, user_data)

                if sample_image:
                    st.image(sample_image, caption=f"Reference Image for {user_name}")

                # Generate image based on user data
                generated_image_url = generate_image(user_data)
                
                # Display the generated image
                st.image(generated_image_url, caption=f"Generated Image for {user_name}")
            else:
                st.error("User not found.")
        
if __name__ == "__main__":
    main()
