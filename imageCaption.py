from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests

# Load pre-trained model and processor from Hugging Face
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Load an image for captioning
img_url = "../compress-img.jpeg"
#image = Image.open(requests.get(img_url, stream=True).raw)
image = Image.open(img_url)

# Process image and generate caption
inputs = processor(image, return_tensors="pt")
output = model.generate(**inputs)
caption = processor.decode(output[0], skip_special_tokens=True)

print(f"Generated caption: {caption}")
