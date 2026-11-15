
from tickets.services.ai_model import get_embedding_model
from tickets.services.ai_text_preprocessing import validate_ai_description


def generate_complaint_embedding(description):
    """
    Convert a valid complaint description into
    a 384-dimensional embedding.

    Returns (embedding, error).
    """

    cleaned, error = validate_ai_description(description)

    if error:
        return None, error

    model = get_embedding_model()

    embedding = model.encode(
        cleaned,
        normalize_embeddings=True,
        convert_to_numpy=True
    )

    return embedding, None
