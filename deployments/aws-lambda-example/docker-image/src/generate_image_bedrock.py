import base64
import os
import random
import boto3
import json

# Define the prompt data for image generation
prompt_data = """
A high-res 4k HDR photo of a golden retriever puppy running on a beach. Action shot, blue sky, white sand, and a big smile. Cinematic film quality.
"""

# Generate a random seed for the generation process
seed = random.randint(0, 100000)

# Define the payload to send to the model
payload = {
    "text_prompts": [{"text": prompt_data}],
    "cfg_scale": 12,
    "seed": seed,
    "steps": 80,  # after 50 steps, pay for premium image
}

# Create the client and invoke the model
bedrock = boto3.client(service_name="bedrock-runtime")
body = json.dumps(payload)
model_id = "stability.stable-diffusion-xl-v0"

# Send the request to the Bedrock API and get the response
response = bedrock.invoke_model(
    body=body,
    modelId=model_id,
    accept="application/json",
    contentType="application/json",
)

# Parse the response and retrieve the image data
response_body = json.loads(response.get("body").read())
artifact = response_body.get("artifacts")[0]
image_encoded = artifact.get("base64").encode("utf-8")
image_bytes = base64.b64decode(image_encoded)

# Define output directory and save the image
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
file_name = f"{output_dir}/generated-{seed}.png"

with open(file_name, "wb") as f:
    f.write(image_bytes)

print(f"Image saved to {file_name}")
