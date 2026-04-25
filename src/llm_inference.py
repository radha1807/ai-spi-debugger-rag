from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_root_cause(log, similar_cases):
    prompt = f"""
    You are an embedded systems expert.

    SPI Log: {log}

    Similar errors:
    {similar_cases}

    Identify the root cause and suggest a fix.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content