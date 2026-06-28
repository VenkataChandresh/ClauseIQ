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


def find_top_matching_chunks(
    question: str, chunks: list[dict], top_k: int = 3
) -> list[dict]:
    question_words = clean_words(question)

    scored_chunks = []

    for chunk in chunks:
        chunk_words = clean_words(chunk["text"])
        score = len(question_words.intersection(chunk_words))

        if score > 0:
            scored_chunks.append(
                {
                    "chunk": chunk,
                    "score": score,
                }
            )

    scored_chunks.sort(key=lambda item: item["score"], reverse=True)

    return scored_chunks[:top_k]
