from groq import AsyncGroq
from app.core.config import settings

client = AsyncGroq(api_key=settings.groq_api_key)

SYSTEM_PROMPT = (
    "You are a strict text rewriter. "
    "Rewrite the text with correct grammar and improved clarity. "
    "Do NOT add any new information. "
    "Preserve the meaning and professional tone. "
    "Keep the rewritten text within ±5% of the original character length. "
    "IMPORTANT: Output ONLY the rewritten text. No explanations, no extra words."
)

async def rewrite_message(original: str):
    user_msg = (
        "Rewrite the following text with correct grammar and better structure. "
        "Output ONLY the rewritten text.\n\n"
        f"{original}"
    )

    resp = await client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
    )

    text = resp.choices[0].message.content

    return text
