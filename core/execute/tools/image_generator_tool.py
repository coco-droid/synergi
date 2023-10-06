from llms.llms import Model
import base64
from PIL import Image
from io import BytesIO
import requests
import os
import uuid
def image_generator_tool(prompt,model):
      dirname = os.path.dirname("/home/t4u/Desktop/suck/synergi/core/")
      static_dir=os.path.join(dirname, "static")
      unique_id = uuid.uuid4()
      image_data=''
      if model=='dalle':
          try:
               image_gen= Model('gpt3')
               image_url=image_gen.generate_dalle(prompt)
               response = requests.get(image_url)
               if response.status_code == 200:
                  file_path = f"{unique_id}.jpg"
                  with open(f"{static_dir}/{file_path}", "wb") as file:
                     file.write(response.content)
                  print(f"Image downloaded and saved as {file_path}")
                  return f"{unique_id}.jpg"
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
        image.save(f"{static_dir}/{unique_id}.png", "PNG")
        print("Image saved successfully.")
        return f"{unique_id}.png"
      except Exception as e:
        print(f"Error: {str(e)}")
 