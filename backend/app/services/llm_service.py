from openai import OpenAI

from app.core.config import (
    OPENROUTER_API_KEY,
    OPENROUTER_MODEL,
    OPENROUTER_BASE_URL,
)

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=OPENROUTER_BASE_URL,
)


def build_context(matches: list[dict]) -> str:
    context_parts = []

    for index, match in enumerate(matches, start=1):
        context_parts.append(f"""
            Source {index}
            Filename: {match["filename"]}
            Chunk Index: {match["chunk_index"]}
            Text:
            {match["text"]}
        """)

    return "\n".join(context_parts)


def generate_answer(question: str, matches: list[dict]) -> str:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set.")

    context = build_context(matches)

    prompt = f"""
        You are ClauseIQ, a legal document question-answering assistant.

        Answer the user's question using only the provided document context.

        Rules:
        - Do not use outside knowledge.
        - If the answer is not in the context, say: "I could not find the answer in the uploaded documents."
        - Keep the answer clear and concise.
        - Mention which source number supports the answer.

        Document Context:
        {context}

        User Question:
        {question}
        """

    completion = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return completion.choices[0].message.content
