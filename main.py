import mlflow
import pathlib
import groq
import dotenv
import os

dotenv.load_dotenv()

# Optional: Set a tracking URI and an experiment name if you have a tracking server
# mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_tracking_uri(f"file://{pathlib.Path.cwd() / 'mlruns'}")
mlflow.set_experiment("Groq")

# Turn on auto tracing for Groq by calling mlflow.groq.autolog()
mlflow.groq.autolog()

client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

# Use the create method to create new message
message = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of low latency LLMs.",
        }
    ],
)

print(message.choices[0].message.content)
