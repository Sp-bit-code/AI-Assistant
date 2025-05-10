
import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep
from io import BytesIO

# Function to open and display images based on a given prompt
def open_images(prompt):
    folder_path = r"Data"  # Folder where the images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores

    # Generate the filenames for the images
    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            # Try to open and display the image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)  # Pause for 1 second before showing the next image
        except IOError as e:
            print(f"Unable to open {image_path}: {e}")

# API details for the Hugging Face Stable Diffusion model
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": f"Bearer {get_key('.env', 'Hugging_FaceAPIKey')}"}

# Async function to send a query to the Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response

# Async function to generate images based on the given prompt
async def generate_images(prompt: str):
    tasks = []

    # Create 4 image generation tasks
    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness maximum, Ultra High details, high resolution, seed {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks to complete
    responses = await asyncio.gather(*tasks)

    # Save the generated images to files
    for i, response in enumerate(responses):
        try:
            os.makedirs("Data", exist_ok=True)  # Ensure the Data directory exists
            filepath = fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg"
            # Check if the response is valid
            if response.status_code == 200:
                image_bytes = response.content
                # Use BytesIO to handle the image data in memory
                img = Image.open(BytesIO(image_bytes))
                img.save(filepath, "JPEG")  # Explicitly save as JPEG
                print(f"Image saved to: {filepath}")  # Added print statement for confirmation
            else:
                print(f"Error generating image {i+1}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error saving image {i+1}: {e}")

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))  # Run the async image generation
    sleep(0.5)  # Add a short delay to allow the OS to fully release the files
    open_images(prompt)  # Open the generated images

# Main loop to monitor for image generation requests
while True:
    try:
        # Read the status and prompt from the data file
        with open(r"C:\Users\LENOVO\Desktop\c++\jarvis\Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        Prompt, Status = Data.split(",")

        # If the status indicates an image generation request
        if Status == "True":
            print("Generating Images... ")
            GenerateImages(prompt=Prompt)

            # Reset the status in the file after generating images
            with open(r"C:\Users\LENOVO\Desktop\c++\jarvis\Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            break  # Exit the loop after processing the request
        else:
            sleep(1)  # Wait for 1 second before checking again
    except Exception as e:
        print(f"An error occurred in the main loop: {e}")
        sleep(5) # Wait longer if there's an error to avoid rapid retries
