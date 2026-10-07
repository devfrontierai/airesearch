import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_synthetic_enterprise_data(num_entities=100, num_documents=500):
    """
    Generates synthetic enterprise data with entities (employees, departments, projects)
    and documents (policies, reports, meeting notes).
    """
    entities = []
    # Departments
    departments = ['Engineering', 'Sales', 'Marketing', 'HR', 'Finance', 'Research']
    for dept in departments:
        entities.append({'id': f'dept_{dept}', 'type': 'department', 'name': dept})
        
    # Projects
    projects = [f'Project_{fake.word().capitalize()}' for _ in range(20)]
    for proj in projects:
        entities.append({'id': f'proj_{proj}', 'type': 'project', 'name': proj, 'status': random.choice(['Active', 'Planning', 'Completed'])})

    # Employees
    for _ in range(num_entities):
        emp_id = f"emp_{fake.unique.random_number(digits=5)}"
        entities.append({
            'id': emp_id,
            'type': 'employee',
            'name': fake.name(),
            'department': f'dept_{random.choice(departments)}',
            'role': fake.job()
        })

    # Documents
    documents = []
    for i in range(num_documents):
        doc_type = random.choice(['policy', 'report', 'memo', 'spec'])
        doc_id = f"doc_{i}"
        
        related_entities = random.sample([e['id'] for e in entities if e['type'] in ('project', 'department', 'employee')], k=random.randint(1, 3))
        
        documents.append({
            'id': doc_id,
            'type': 'document',
            'doc_type': doc_type,
            'title': fake.catch_phrase(),
            'content': fake.text(max_nb_chars=500),
            'timestamp': fake.date_time_between(start_date="-1y", end_date="now").isoformat(),
            'related_entities': related_entities
        })
        
    return entities, documents

if __name__ == "__main__":
    e, d = generate_synthetic_enterprise_data(10, 20)
    print(f"Generated {len(e)} entities and {len(d)} documents.")
