import os
import json
import numpy as np
from django.conf import settings
from openai import OpenAI

BASE_DIR = os.path.dirname(__file__)

FAQ_PATH = os.path.join(BASE_DIR, "faq_dataset.json")
EMBED_PATH = os.path.join(BASE_DIR, "faq_embeddings.json")

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def embed_text(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def load_dataset():
    if not os.path.exists(FAQ_PATH):
        return []
    with open(FAQ_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_embeddings(embeddings):
    with open(EMBED_PATH, "w", encoding="utf-8") as f:
        json.dump(embeddings, f)


def load_embeddings():
    if not os.path.exists(EMBED_PATH):
        return []
    with open(EMBED_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def build_embeddings():
    dataset = load_dataset()

    if not dataset:
        return []

    embeddings = []

    print("Embedding dataset building...")

    for item in dataset:
        emb = embed_text(item["answer"])
        embeddings.append(emb)

    save_embeddings(embeddings)

    print("Embedding дайын")

    return embeddings


def semantic_search(question, threshold=0.75):
    dataset = load_dataset()
    embeddings = load_embeddings()

    if not embeddings:
        embeddings = build_embeddings()

    question_embedding = embed_text(question)

    similarities = [
        cosine_similarity(question_embedding, emb)
        for emb in embeddings
    ]

    best_score = max(similarities)
    best_index = similarities.index(best_score)

    if best_score > threshold:
        return dataset[best_index]["answer"]

    return None