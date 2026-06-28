SESSION_STORE = {}


def save_session_chunks(session_id: str, chunks: list[dict]) -> None:
    SESSION_STORE[session_id] = chunks


def get_session_chunks(session_id: str) -> list[dict] | None:
    return SESSION_STORE.get(session_id)
