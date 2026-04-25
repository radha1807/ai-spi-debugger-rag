from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def get_root_cause(log: str, similar_cases: list[str]) -> str:
    """
    Call GPT-4o-mini with the current log + retrieved similar cases.
    Returns a diagnosis string.
    Falls back to a simple rule-based diagnosis if the API call fails.
    """
    if not similar_cases:
        similar_text = "No similar historical cases found."
    else:
        similar_text = "\n".join(f"- {c}" for c in similar_cases)

    prompt = f"""You are an expert in embedded systems and SPI (Serial Peripheral Interface) communication debugging.

You are given a raw SPI log line and a set of similar historical error cases retrieved from a knowledge base.

Your job:
1. Identify the most likely root cause of the issue in the log.
2. Suggest a concrete fix or next debugging step.
3. Rate your confidence: High / Medium / Low.

SPI Log:
{log}

Similar historical cases:
{similar_text}

Respond in this exact format:
Root Cause: <your analysis>
Fix: <your suggestion>
Confidence: <High | Medium | Low>
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # Low temp = more deterministic for debugging
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"[LLM ERROR] API call failed: {e}")
        return _fallback_diagnosis(log)


def _fallback_diagnosis(log: str) -> str:
    """Rule-based fallback if LLM is unavailable."""
    if "ERR" in log:
        return (
            "Root Cause: Possible SPI communication failure — timing mismatch, noise, or bad CS signal.\n"
            "Fix: Check clock polarity/phase (CPOL/CPHA) settings and signal integrity.\n"
            "Confidence: Low"
        )
    elif "TIMEOUT" in log:
        return (
            "Root Cause: Slave device not responding within expected window.\n"
            "Fix: Verify wiring, check chip select line, confirm slave is powered.\n"
            "Confidence: Low"
        )
    else:
        return (
            "Root Cause: No obvious error pattern detected.\n"
            "Fix: Cross-check with oscilloscope trace.\n"
            "Confidence: Low"
        )
