
from openai import OpenAI
import base64
from PIL import Image
from io import BytesIO

client = OpenAI()
response = client.images.generate(
  model="dall-e-2",
  prompt="A cute baby sea otter",
  n=2,
  size="1024x1024",
  response_format="b64_json"
)

print("Image created time:{}".format(response.created))
for img in response.data:
  img_b64 = img.b64_json
  img_bytes = base64.b64decode(img_b64)
  img = Image.open(BytesIO(img_bytes))
  img.show()
