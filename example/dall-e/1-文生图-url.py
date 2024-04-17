
from openai import OpenAI
from PIL import Image
import requests
from io import BytesIO

client = OpenAI()
response = client.images.generate(
  model="dall-e-3",
  prompt="a white siamese cat",
  size="1024x1024",
  quality="standard",
)
image_url = response.data[0].url
response = requests.get(image_url)
image = Image.open(BytesIO(response.content))
image.show()