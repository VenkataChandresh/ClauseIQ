import chromadb

chroma_client = chromadb.Client()


def get_collection_name(session_id: str) -> str:
    return f"session_{session_id.replace('-', '_')}"


def get_or_create_session_collection(session_id: str):
    collection_name = get_collection_name(session_id)
    return chroma_client.get_or_create_collection(name=collection_name)


def add_chunks_to_chroma(session_id: str, chunks: list[dict]) -> None:
    collection = get_or_create_session_collection(session_id)

    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        chunk_id = f"{session_id}_{chunk['filename']}_{chunk['chunk_index']}"

        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append(
            {
                "session_id": session_id,
                "filename": chunk["filename"],
                "chunk_index": chunk["chunk_index"],
            }
        )

    if ids:
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )


def query_session_chroma(session_id: str, question: str, top_k: int = 3) -> list[dict]:
    collection = get_or_create_session_collection(session_id)

    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    matches = []

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for document, metadata, distance in zip(documents, metadatas, distances):
        matches.append(
            {
                "text": document,
                "filename": metadata["filename"],
                "chunk_index": metadata["chunk_index"],
                "distance": distance,
            }
        )

    return matches
