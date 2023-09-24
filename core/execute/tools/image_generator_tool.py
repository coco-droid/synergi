from llms.llms import Model
import base64
from PIL import Image
from io import BytesIO
import requests

def generate_image(prompt,model):
      image_data=''
      if model=='dalle':
          try:
               image_gen= Model('gpt3')
               image_url=image_gen.generate_dalle(prompt)
               response = requests.get(image_url)
               if response.status_code == 200:
                  file_path = "downloaded_image.jpg"
                  with open(file_path, "wb") as file:
                     file.write(response.content)
                  print(f"Image downloaded and saved as {file_path}")
               else:
                  print(f"Failed to download image. Status code: {response.status_code}")
          except Exception as e:
                print(f"Error lk: {str(e)}")
      elif model=='dalle_clarifai':
        image_gen= Model('gpt3')
        image_data=image_gen.generate_image_dalle(prompt)
      elif model=='stablediff':
        image_gen= Model('gpt3')
        image_data=image_gen.generate_image_with_text(prompt)
      if not image_data:
        if(model=='dalle'):
           print('the image was downloaded')
        else:
           print("No image data received.")
           return
      try:
        binary_io = BytesIO(image_data)
        image = Image.open(binary_io)
        image.save("output1.png", "PNG")
        print("Image saved successfully.")
      except Exception as e:
        print(f"Error: {str(e)}")
 