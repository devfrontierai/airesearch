import matplotlib.pyplot as plt

# Data from our experiment
documents = [500, 10000, 100000]
rag_time = [0.000035, 0.000760, 0.008247]
cci_time = [0.000354, 0.000838, 0.002449]

plt.figure(figsize=(8, 6))
plt.plot(documents, rag_time, marker='o', label='Baseline RAG (O(N) Scan)', linewidth=2, color='#e74c3c', markersize=8)
plt.plot(documents, cci_time, marker='s', label='CCI (O(E) Graph Fetch)', linewidth=2, color='#2ecc71', markersize=8)

plt.xscale('log')
plt.yscale('log')
plt.xlabel('Number of Enterprise Documents in System', fontsize=12)
plt.ylabel('Retrieval Latency (Seconds)', fontsize=12)
plt.title('Asymptotic Scaling: RAG vs. Continuous Context Intelligence', fontsize=14, fontweight='bold')
plt.legend(fontsize=12)
plt.grid(True, which="both", ls="--", alpha=0.5)

plt.tight_layout()
plt.savefig('scaling_results.png', dpi=300)
print("Plot saved as scaling_results.png")
