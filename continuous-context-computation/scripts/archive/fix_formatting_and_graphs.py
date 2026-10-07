import os
import shutil

def fix_formatting_and_graphs():
    paper_dir = r"c:\PRODDEV\devfrontier\airesearch\ccicompute\paper"
    results_dir = r"c:\PRODDEV\devfrontier\airesearch\ccicompute\results\plots"

    # 1. COPY IMAGE TO PAPER DIRECTORY FOR EASY INCLUSION
    src_image = os.path.join(results_dir, "large_scale_performance.png")
    dst_image = os.path.join(paper_dir, "large_scale_performance.png")
    if os.path.exists(src_image):
        shutil.copy(src_image, dst_image)

    # 2. UPDATE MAIN.TEX (Add microtype to fix ugly hyphenations like Do-Main)
    main_path = os.path.join(paper_dir, "main.tex")
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if r"\usepackage{microtype}" not in content:
        content = content.replace(r"\usepackage{times}", "\\usepackage{times}\n\\usepackage{microtype}")
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(content)

    # 3. FIX RAG DIAGRAM OVERLAP (Use figure* and horizontal layout)
    with open(os.path.join(paper_dir, "02_introduction.tex"), 'w', encoding='utf-8') as f:
        f.write(r"""
\section{Introduction and Problem Domain}
\label{sec:intro}
The core research question of this study investigates whether continuously computed and maintained semantic context can fundamentally resolve the geometric and computational bottlenecks inherent to traditional Retrieval-Augmented Generation (RAG).

\subsection{The Architectural Limits of Standard RAG}
Traditional RAG systems treat context assembly as a strictly query-time operation. When a user issues a query, the system embeds the text, performs an Approximate Nearest Neighbor (ANN) search over an unstructured Vector Database, retrieves $K$ discrete text chunks, and concatenates them into an LLM's prompt window. 

While effective for localized, single-document retrieval, this architecture catastrophically degrades in complex enterprise environments. First, unstructured vector similarity search inherently suffers from $O(N)$ scalability limits. As the enterprise corpus $N$ scales, the geometric distance between semantic concepts begins to collapse, leading to "embedding dilution".

\begin{figure*}[htbp]
\centering
\begin{tikzpicture}[
    node distance=3.5cm, auto, scale=0.85, transform shape,
    box/.style={rectangle, draw, fill=red!10, text width=3cm, text centered, rounded corners, minimum height=1.2cm},
    arrow/.style={thick,->,>=stealth}
]
\node (query) [box] {1. User Query (Online)};
\node (embed) [box, right of=query] {2. Embedding (Latency)};
\node (vdb) [box, right of=embed] {3. Vector DB Scan ($O(N)$)};
\node (chunks) [box, right of=vdb] {4. Disconnected Chunks};
\node (llm) [box, right of=chunks] {5. LLM Window (Lost in Middle)};

\draw [arrow] (query) -- (embed);
\draw [arrow] (embed) -- (vdb);
\draw [arrow] (vdb) -- (chunks);
\draw [arrow] (chunks) -- (llm);
\end{tikzpicture}
\caption{Standard RAG Architecture. The linear $O(N)$ retrieval bottleneck occurs entirely at query time.}
\label{fig:rag_issues}
\end{figure*}

Second, standard RAG fails at cross-system multi-hop reasoning. If an answer requires linking a Slack message to a Jira ticket, traditional RAG must either rely on the LLM's internal reasoning to bridge the chunks, or employ iterative agentic loops which compound latency.
""")

    # 4. FIX CCC DIAGRAM OVERLAP
    with open(os.path.join(paper_dir, "02b_ccc_architecture.tex"), 'w', encoding='utf-8') as f:
        f.write(r"""
\section{Continuous Context Computation (CCC)}
\label{sec:ccc}

To resolve the query-time bottlenecks of RAG, we propose \textbf{Continuous Context Computation (CCC)}. CCC formally decouples context computation from inference computation.

\subsection{The CCC Algorithmic Framework}
Data streams from disparate systems are ingested asynchronously. The CCC engine continuously extracts entities, resolves schemas, and computes relational edges in the background, maintaining a highly structured, temporally-aware Semantic Graph.

At query time, the system no longer performs a linear $O(N)$ scan. It identifies starting nodes within the pre-computed graph and traverses the explicitly maintained edges $E$. This reduces retrieval complexity to a localized $O(E)$ graph neighborhood traversal.

\begin{figure*}[htbp]
\centering
\begin{tikzpicture}[
    node distance=4cm, auto, scale=0.85, transform shape,
    box/.style={rectangle, draw, fill=blue!10, text width=4cm, text centered, rounded corners, minimum height=1.2cm},
    widebox/.style={rectangle, draw, fill=green!10, text width=4cm, text centered, rounded corners, minimum height=1.2cm},
    arrow/.style={thick,->,>=stealth}
]
\node (data) [widebox] {Enterprise Streams (Async)};
\node (engine) [widebox, right of=data] {Context Engine (Offline)};
\node (graph) [widebox, right of=engine] {Semantic Graph ($O(E)$)};
\node (query) [box, fill=yellow!20, above of=graph, yshift=-2cm] {User Query};
\node (llm) [box, fill=yellow!20, right of=graph] {Instant LLM Response};

\draw [arrow] (data) -- (engine);
\draw [arrow] (engine) -- (graph);
\draw [arrow] (query) -- (graph);
\draw [arrow] (graph) -- (llm);
\end{tikzpicture}
\caption{Continuous Context Computation (CCC) Architecture. Semantic computation is shifted offline, enabling $O(E)$ query-time traversal.}
\label{fig:ccc_arch}
\end{figure*}

By executing semantic alignment before the user asks a question, CCC achieves flat latency scaling and perfect provenance tracking.
""")

    # 5. FIX DATASET SPACING AND IMPLEMENT THE 3 GROUPS
    with open(os.path.join(paper_dir, "03_benchmark_strategy.tex"), 'w', encoding='utf-8') as f:
        f.write(r"""
\section{Benchmark Strategy and Datasets}
\label{sec:benchmark}
To robustly evaluate the CCC hypothesis, our framework employs public benchmarks and three meticulously generated synthetic enterprise groups.

\subsection{Public Benchmark Formalization}
\textbf{Dataset 1: MS MARCO.} We evaluate $P@K$ and $nDCG@10$ across training queries to establish standard search baselines.

\textbf{Dataset 2: HotpotQA.} We evaluate multi-hop chaining across 90,447 questions requiring exactly two supporting facts $f_1, f_2$. 

\subsection{Synthetic Enterprise Generation (3 Target Modalities)}
To prove CCC's versatility, we generated 512,000 documents segregated into three distinct modalities.

\textbf{Group 1: Unstructured Sources Only.} 
This represents raw communication streams (e.g., Slack, Gmail, Fireflies transcripts). CCC continuously ingests these unstructured blocks, extracting Named Entities via NLP pipelines, and linking overlapping entities (e.g., linking a mention of "Project Phoenix" in Slack to a meeting transcript in Fireflies).

\textbf{Group 2: Hybrid (Structured + Unstructured).} 
This group tests the integration of rigid schema data with free-form text. For example, linking a structured PostgreSQL row representing a customer's \texttt{annual\_contract\_value} directly to an unstructured Jira bug ticket complaining about that customer's login issue. CCC handles this by treating structured primary keys as absolute anchor nodes, wrapping unstructured text edges around them.

\textbf{Group 3: Structured Sources Only.} 
This isolates CCC's ability to perform \textit{Semantic Schema Alignment} across disconnected databases. 
For instance, a CRM system uses \texttt{customer\_id} and \texttt{annual\_value}, while the ERP system uses \texttt{cust\_id} and \texttt{revenue}. Query-time RAG approaches fail here without heavy LLM "text-to-SQL" reasoning. CCC continuously maps these heterogeneous schemas into a unified, agnostic node structure offline, allowing instant traversal across databases without writing complex JOINs.
""")

    # 6. INJECT RESULT GRAPH
    tex_06 = os.path.join(paper_dir, "06_metrics_efficiency.tex")
    with open(tex_06, 'r', encoding='utf-8') as f:
        content_06 = f.read()
    
    if "large_scale_performance.png" not in content_06:
        graph_tex = r"""
\begin{figure*}[htbp]
\centering
\includegraphics[width=0.8\textwidth]{large_scale_performance.png}
\caption{Benchmark Latency Results: Comparing Dense RAG vs. CCC across Public Datasets and the 512K Synthetic Enterprise Corpus. CCC maintains a flat O(E) latency profile regardless of the total document scale.}
\label{fig:results_graph}
\end{figure*}
"""
        content_06 = content_06.replace(r"\subsection{Mathematical Proof of O(E) Superiority}", graph_tex + "\n" + r"\subsection{Mathematical Proof of O(E) Superiority}")
        with open(tex_06, 'w', encoding='utf-8') as f:
            f.write(content_06)

    print("Formatting fixed: Diagrams spanned, microtype added, dataset groups mapped, and result graph injected.")

if __name__ == "__main__":
    fix_formatting_and_graphs()
