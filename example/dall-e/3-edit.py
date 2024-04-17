from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO

client = OpenAI()
response = client.images.edit(model="dall-e-2", image=open("image.png","rb"),
  mask=open("mask.png","rb"),
  prompt = ("A serene landscape,mountain lake surrounded by lush green forests under a clear blue sky. "
            "There is a big red hot air Balloon flowing."),)
img_url = response.data[0].url
res = requests.get(img_url)
image = Image.open(BytesIO(res.content))
image.show()