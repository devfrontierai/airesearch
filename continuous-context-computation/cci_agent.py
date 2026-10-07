from context_manager import ContinuousContextManager

class CCIAgent:
    def __init__(self, context_manager: ContinuousContextManager):
        self.context_manager = context_manager
        
    def answer_query(self, query_entity: str, query_text: str):
        # 1. Evaluate context fitness
        fitness = self.context_manager.evaluate_context_fitness(query_entity)
        if fitness < 0.5:
            print(f"Agent: Context fitness low ({fitness:.2f}). Triggering background refresh...")
            # In a real system, this triggers a data pipeline refresh
            
        # 2. Retrieve context
        context = self.context_manager.get_context_for_agent(query_entity)
        
        # 3. Formulate answer (Simulated LLM call)
        response = f"Based on the following context, I have answered your query:\n{context[:150]}..."
        return response
