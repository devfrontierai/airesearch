def simple_rag_retrieve(query_entity, documents):
    """Simulates a simple vector/keyword search for RAG."""
    return [d for d in documents if query_entity in d.get('related_entities', [])]
