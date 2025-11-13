import asyncio
from functools import partial
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en")

async def generate_embedding(text: str):
    loop = asyncio.get_running_loop()
    vector = await loop.run_in_executor(None, partial(model.encode, text, normalize_embeddings=True))
    return vector.tolist()
