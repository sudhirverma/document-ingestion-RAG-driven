from transformers import pipeline

model = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")

def generate_embedding(content: str):
    return model(content)[0]