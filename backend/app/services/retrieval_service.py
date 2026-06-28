import re

STOP_WORDS = {
    "what",
    "where",
    "when",
    "who",
    "why",
    "how",
    "is",
    "are",
    "do",
    "does",
    "did",
    "the",
    "a",
    "an",
    "show",
    "tell",
    "me",
    "listed",
    "mentioned",
}


def clean_words(text: str) -> set[str]:
    words = re.findall(r"\b\w+\b", text.lower())
    return {word for word in words if word not in STOP_WORDS}


def find_best_matching_chunk(question: str, chunks: list[dict]) -> dict | None:
    question_words = clean_words(question)

    best_chunk = None
    best_score = 0

    for chunk in chunks:
        chunk_words = clean_words(chunk["text"])
        score = len(question_words.intersection(chunk_words))

        if score > best_score:
            best_score = score
            best_chunk = chunk

    if best_chunk is None:
        return None

    return {
        "chunk": best_chunk,
        "score": best_score,
    }
