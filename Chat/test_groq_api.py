from groq import Groq

client = Groq(api_key="YOUR_API_KEY")

completion = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Explain LLM"
        }
    ],
    temperature=0.7,
    max_completion_tokens=300,
    stream=True
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")