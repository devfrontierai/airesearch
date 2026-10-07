from graph_store import GraphStore
from typing import List, Dict, Any
from datetime import datetime

class ContinuousContextManager:
    def __init__(self, store: GraphStore):
        self.store = store
        self.last_update = datetime.now()
        
    def ingest_entities(self, entities: List[Dict[str, Any]]):
        for e in entities:
            self.store.add_node(e['id'], **e)
            
    def ingest_documents(self, documents: List[Dict[str, Any]]):
        for d in documents:
            self.store.add_node(d['id'], **d)
            for e_id in d.get('related_entities', []):
                self.store.add_edge(d['id'], e_id, "MENTIONS")
                self.store.add_edge(e_id, d['id'], "IS_MENTIONED_IN")
                
    def evaluate_context_fitness(self, query_entity: str) -> float:
        """
        Evaluate if the context subgraph for a query entity is fit (fresh, complete).
        Returns a score between 0.0 and 1.0.
        """
        subgraph = self.store.get_context_subgraph(query_entity, depth=1)
        if len(subgraph.nodes) == 0:
            return 0.0
            
        # Simplified fitness function based on node count and presence of docs
        doc_count = sum(1 for n, d in subgraph.nodes(data=True) if d.get('type') == 'document')
        
        fitness = min(1.0, doc_count / 5.0)
        return fitness
        
    def get_context_for_agent(self, query_entity: str):
        """Retrieve pre-computed context."""
        subgraph = self.store.get_context_subgraph(query_entity, depth=2)
        
        # Serialize subgraph to text for the agent
        context_str = f"Context for {query_entity}:\n"
        for node, data in subgraph.nodes(data=True):
            if data.get('type') == 'document':
                context_str += f"- Doc [{data.get('title')}]: {data.get('content')[:100]}...\n"
            else:
                context_str += f"- Entity [{data.get('type')}]: {data.get('name')}\n"
        return context_str
