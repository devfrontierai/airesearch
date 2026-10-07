import time
from data_generator import generate_synthetic_enterprise_data
from graph_store import GraphStore
from context_manager import ContinuousContextManager

def simulate_retrieval_at_scale(num_entities, num_documents):
    print(f"\n--- Scaling Test: {num_documents} Documents ---")
    entities, documents = generate_synthetic_enterprise_data(num_entities, num_documents)
    
    store = GraphStore()
    manager = ContinuousContextManager(store)
    manager.ingest_entities(entities)
    manager.ingest_documents(documents)
    
    query_entity = entities[0]['id']
    
    # Baseline RAG simulation (Linear scan simulating vector DB filtering without index, or keyword scan)
    # At scale, this represents the O(N) cost of searching/filtering unstructured data
    start_time = time.time()
    rag_context = [d for d in documents if query_entity in d.get('related_entities', [])]
    rag_retrieval_time = time.time() - start_time
    
    # CCI retrieval (Graph neighborhood fetch O(E) where E is local connections, not N)
    start_time = time.time()
    cci_context = manager.get_context_for_agent(query_entity)
    cci_retrieval_time = time.time() - start_time
    
    print(f"RAG Retrieval Time : {rag_retrieval_time:.6f} sec")
    print(f"CCI Retrieval Time : {cci_retrieval_time:.6f} sec")
    
    return rag_retrieval_time, cci_retrieval_time

def run_scaling_experiment():
    print("Running Scaling Benchmark to demonstrate asymptotic complexity...")
    
    scales = [
        (100, 500),
        (1000, 10000),
        (5000, 100000)
    ]
    
    for entities_count, docs_count in scales:
        simulate_retrieval_at_scale(entities_count, docs_count)

if __name__ == "__main__":
    run_scaling_experiment()
