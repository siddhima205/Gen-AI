# gen-ai
The individual files in this repositiry aim at utilizing various gen ai models and implementing them in code.

1.streamlitColorDetectionUsingPixtral: Uses Pixtral from mistral. This model helps understand the color and type of image uploaded.It can be used to detect faults in the product description by comparing the color and type of image. It also uses fuzzy logic to get a similarity index on attributes returned from Gen AI and attributes defined.

2. runwayCreateVideoFromImages: This uses runway model . The runway model expects a excel as an input with image path and prompt. Using the prompt, then runway package creates a video from the image passed. This video is then played on the straemlit app and can be downloaded to your local system.

3. streamlitChat: This uses mistral model(can be switched to llama models as well). The code takes few attributes as input and creates a description for the product.

