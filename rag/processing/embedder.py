from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        if not isinstance(texts, list):
            raise TypeError("texts must be a list of strings")

        if not all(isinstance(text, str) for text in texts):
            raise TypeError("all texts must be strings")

        return self.model.encode(texts)