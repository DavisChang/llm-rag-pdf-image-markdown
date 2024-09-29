from dataclasses import dataclass


@dataclass
class QueryResponse:
    query_text: str
    response_text: str


def query_rag(query_text: str) -> QueryResponse:
    return QueryResponse(query_text=query_text, response_text="query_rag")


if __name__ == "__main__":
    query_rag("How much does a landing page cost to develop?")
