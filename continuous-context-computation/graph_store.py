import networkx as nx
from typing import List, Dict, Any

class GraphStore:
    def __init__(self):
        self.graph = nx.MultiDiGraph()
        
    def add_node(self, node_id: str, **attributes):
        self.graph.add_node(node_id, **attributes)
        
    def add_edge(self, source: str, target: str, relationship: str, **attributes):
        self.graph.add_edge(source, target, relationship=relationship, **attributes)
        
    def update_node(self, node_id: str, **attributes):
        if self.graph.has_node(node_id):
            for k, v in attributes.items():
                self.graph.nodes[node_id][k] = v
                
    def get_node(self, node_id: str) -> Dict[str, Any]:
        return self.graph.nodes[node_id] if self.graph.has_node(node_id) else None

    def get_context_subgraph(self, root_id: str, depth: int = 2) -> nx.MultiDiGraph:
        """Extract a local neighborhood around a node to serve as context."""
        if not self.graph.has_node(root_id):
            return nx.MultiDiGraph()
            
        nodes = {root_id}
        for _ in range(depth):
            neighbors = set()
            for n in nodes:
                neighbors.update(self.graph.successors(n))
                neighbors.update(self.graph.predecessors(n))
            nodes.update(neighbors)
            
        return self.graph.subgraph(nodes).copy()
