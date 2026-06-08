import requests

API_KEY = "sk-x7kgNjYYxHjdmyWWe41evExxuPm4v1u2okDGT3YaasRCrQaQ"

url = "https://api.stability.ai/v2beta/stable-image/generate/core"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*"
}

files = {
    "prompt": (None, "a girl just watching the moon on night")
}

response = requests.post(
    url,
    headers=headers,
    files=files
)

if response.status_code == 200:
    with open("generated_image.png", "wb") as f:
        f.write(response.content)
    print("Image saved as generated_image.png")
else:
    print("Error:", response.status_code)
    print(response.text)