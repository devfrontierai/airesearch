# Continuous Context Computation (CCC) for Enterprise AI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Paper: LaTeX](https://img.shields.io/badge/Paper-LaTeX-blue)](paper/continuous-context-computation-researchpaper.tex)

This repository contains the official codebase, synthetic datasets, benchmark algorithms, and the full 7-page LaTeX research paper evaluating **Continuous Context Computation (CCC)**. 

Our core research hypothesis investigates whether continuously computed and maintained semantic context can fundamentally resolve the geometric and computational bottlenecks inherent to traditional Retrieval-Augmented Generation (RAG). By shifting entity extraction and schema alignment to an asynchronous background engine, CCC transforms the online retrieval penalty from a massive $O(N)$ vector scan into a flat $O(E)$ localized graph traversal.

---

## 🧬 Core Experiments & Dataset Modalities

To robustly evaluate the CCC framework against standard Dense RAG and Hybrid RAG baselines, we evaluate performance across **2 Public Benchmarks** (MS MARCO, HotpotQA) and a **512,000-Document Synthetic Enterprise Corpus** separated into 3 distinct integration modalities:

1. **Unstructured Sources Only:** Raw communication streams (e.g., Slack, Gmail, Fireflies transcripts) processed via continuous NLP entity extraction.
2. **Hybrid (Structured + Unstructured):** Linking rigid schema data (e.g., PostgreSQL rows) to free-form text (e.g., Jira bug tickets).
3. **Structured Sources Only:** Semantic schema alignment between disconnected databases (e.g., mapping an ERP's `cust_id` to a CRM's `customer_id` without LLM Text-to-SQL logic).

### ⚡ Federated Pointer Nodes (Runtime Compute)
The repository also includes experiments detailing **Federated CCC**. For highly volatile or zero-trust siloed data (e.g., live stock APIs) that cannot be pre-computed offline, the engine creates structural "Pointers." At query time, the traversal triggers a synchronous $O(1)$ runtime fetch, demonstrating that CCC remains robust even when pure pre-computation is impossible.

---

## 📂 Repository Structure

```text
continuous-context-computation/
├── data/
│   ├── public/              # Cache for HF datasets (HotpotQA, MS MARCO)
│   └── synthetic/           # Output for the generated 512K enterprise corpus
├── paper/
│   ├── continuous-context-computation-researchpaper.tex  # Main LaTeX entrypoint
│   ├── references.bib                                    # Real-world academic citations
│   └── *.tex                                             # Modular sections (Intro, Taxonomy, etc.)
├── results/
│   ├── logs/                # Raw CSV/JSON benchmark traces
│   └── plots/               # Matplotlib performance graphs (Latency, F1, Scaling)
├── scripts/
│   ├── run_full_scale_benchmarks.py   # Main pipeline for 512K scale tests
│   ├── generate_final_assets.py       # Matplotlib & diagram generation
│   └── archive/                       # Historical structural formatting scripts
└── src/                     # Core CCC Framework & Baseline implementations
```

---

## 🚀 How to Reproduce the Research

### 1. Environment Setup
We recommend Python 3.10+. Install the necessary scientific dependencies:
```bash
python -m venv \venv
.\venv\Scripts\activate
pip install datasets networkx numpy matplotlib
```

### 2. Execute Benchmarks
Run the full-scale simulation. This script generates the synthetic corpus, loads the public data, and executes all 6 architectural baselines across the 12-level Question Taxonomy:
```bash
python scripts/run_full_scale_benchmarks.py
```

### 3. Generate Visual Assets
Once the benchmarks have completed, generate the comparative analytics (Latency Log-Scale charts, Accuracy metrics, and $O(N)$ vs $O(E)$ line graphs). This script also embeds the highly polished TikZ architecture diagrams for the paper:
```bash
python scripts/generate_final_assets.py
```

### 4. Compile the Research Paper
The full 7-page academic paper is written in IEEE/ACL double-column formatting using LaTeX. You can compile it using `latexmk` or `pdflatex`.

If using **VS Code with LaTeX Workshop**:
1. Open `paper/continuous-context-computation-researchpaper.tex`
2. Select the `Recipe: pdflatex -> bibtex -> pdflatex * 2` tool.
3. The resulting `continuous-context-computation-researchpaper.pdf` will contain all generated charts, mathematical proofs, federated extension data, and architecture diagrams.

---
*Developed by the DevFrontier AI Research Division.*
