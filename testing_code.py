import requests
from PIL import Image
from io import BytesIO

# Cloudinary image URL
image_url = "http://res.cloudinary.com/deifbikqu/image/upload/v1710743455/qajtzi7cjkjau96q6w01.png"

# Fetch the image from Cloudinary
response = requests.get(image_url)

if response.status_code == 200:
    # Convert the response content into a PIL image
    img = Image.open(BytesIO(response.content))
    
    # Save the image to a local file
    img.save("cloudinary_image.png")
    print("Image saved successfully.")
else:
    print("Failed to fetch image from Cloudinary.")
