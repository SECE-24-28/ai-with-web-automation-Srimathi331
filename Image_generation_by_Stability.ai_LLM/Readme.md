# AI Image Generator using Stability AI API

## Overview

This project demonstrates how to generate images from text prompts using the Stability AI Image Generation API. The script sends a user-provided prompt to the Stability AI model, receives the generated image as a response, and saves it locally on the system.

The goal of this project is to understand how image generation APIs work and how they can be integrated into Python applications.

---

## Technologies Used

* Python
* Requests Library
* Stability AI API

---

## Project Workflow

### Step 1: Import Required Library

The `requests` library is used to send HTTP requests to the Stability AI API.

```python
import requests
```

---

### Step 2: Configure API Key

An API key is required to authenticate requests with Stability AI.

```python
API_KEY = "YOUR_API_KEY"
```

The API key is included in the request headers to verify access permissions.

---

### Step 3: Define API Endpoint

The image generation endpoint is specified using the API URL.

```python
url = "https://api.stability.ai/v2beta/stable-image/generate/core"
```

This endpoint accepts a text prompt and returns a generated image.

---

### Step 4: Create Request Headers

Headers contain the authentication token and specify the expected response type.

```python
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "image/*"
}
```

---

### Step 5: Provide the Image Prompt

The prompt describes the image that should be generated.

```python
files = {
    "prompt": (None, "a girl just watching the moon on night")
}
```

The quality and relevance of the generated image depend heavily on the prompt provided.

---

### Step 6: Send API Request

A POST request is sent to the Stability AI server.

```python
response = requests.post(
    url,
    headers=headers,
    files=files
)
```

The API processes the prompt and generates an image based on the description.

---

### Step 7: Handle the Response

If the request is successful, the image is saved locally.

```python
if response.status_code == 200:
```

The generated image is written into a PNG file.

```python
with open("generated_image.png", "wb") as f:
    f.write(response.content)
```

---

### Step 8: Error Handling

If the request fails, the script displays the error code and message.

```python
else:
    print("Error:", response.status_code)
    print(response.text)
```

This helps in debugging issues such as invalid API keys, insufficient credits, or malformed requests.

---

## Workflow Diagram

```text
User Prompt
      │
      ▼
Python Script
      │
      ▼
Stability AI API Request
      │
      ▼
Image Generation Model
      │
      ▼
Generated Image Response
      │
      ▼
Save as generated_image.png
```

---

## Expected Output

After successful execution, a file named:

```text
generated_image.png
```

will be created in the project directory containing the AI-generated image based on the provided prompt.

---

## Learning Outcomes

Through this project, you will learn:

* How REST APIs work
* API authentication using bearer tokens
* Sending POST requests in Python
* Handling binary image responses
* Saving generated images locally
* Basic integration of Generative AI services into applications

---

## Future Improvements

Some possible enhancements include:

* Taking prompts as user input
* Creating a simple web interface using Flask or Streamlit
* Supporting multiple image generations
* Allowing users to select image styles and dimensions
* Storing generated images in cloud storage

---

## Note

For security reasons, API keys should not be hardcoded in production applications. Consider storing them in environment variables or a `.env` file.
