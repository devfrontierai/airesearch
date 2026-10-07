import os

def refine_paper():
    paper_dir = r"c:\PRODDEV\devfrontier\airesearch\ccicompute\paper"

    # 1. UPDATE MAIN.TEX TO INCLUDE TIKZ AND LISTINGS
    main_path = os.path.join(paper_dir, "main.tex")
    with open(main_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if r"\usepackage{tikz}" not in content:
        tikz_pkg = "\\usepackage{tikz}\n\\usetikzlibrary{shapes.geometric, arrows, positioning}\n\\usepackage{listings}\n\\lstset{breaklines=true, basicstyle=\\ttfamily\\footnotesize}\n"
        content = content.replace(r"\usepackage{cleveref}", "\\usepackage{cleveref}\n" + tikz_pkg)
        
    if r"\input{02b_ccc_architecture.tex}" not in content:
        content = content.replace(r"\input{02_introduction.tex}", "\\input{02_introduction.tex}\n\\input{02b_ccc_architecture.tex}")
        
    with open(main_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # 2. REWRITE INTRODUCTION: RAG Problem Domain & Diagram (Replacing year-by-year bloat)
    with open(os.path.join(paper_dir, "02_introduction.tex"), 'w', encoding='utf-8') as f:
        f.write(r"""
\section{Introduction and Problem Domain}
\label{sec:intro}
The core research question of this study investigates whether continuously computed and maintained semantic context can fundamentally resolve the geometric and computational bottlenecks inherent to traditional Retrieval-Augmented Generation (RAG).

\subsection{The Architectural Limits of Standard RAG}
Traditional RAG systems treat context assembly as a strictly query-time operation. When a user issues a query, the system embeds the text, performs an Approximate Nearest Neighbor (ANN) search over an unstructured Vector Database, retrieves $K$ discrete text chunks, and concatenates them into an LLM's prompt window. 

While effective for localized, single-document retrieval, this architecture catastrophically degrades in complex enterprise environments.
First, unstructured vector similarity search inherently suffers from $O(N)$ scalability limits. As the enterprise corpus $N$ scales, the geometric distance between semantic concepts begins to collapse, leading to "embedding dilution" where highly relevant but sparsely worded evidence is outranked by verbose, tangentially related chunks.

\begin{figure}[h]
\centering
\begin{tikzpicture}[
    node distance=1.3cm, auto, scale=0.8, transform shape,
    box/.style={rectangle, draw, fill=red!10, text width=6cm, text centered, rounded corners, minimum height=0.8cm},
    arrow/.style={thick,->,>=stealth}
]
\node (query) [box] {1. User Query (Online)};
\node (embed) [box, below of=query] {2. Embedding Model (Latency Bottleneck)};
\node (vdb) [box, below of=embed] {3. Vector DB Scan ($O(N)$ Complexity)};
\node (chunks) [box, below of=vdb] {4. Disconnected Unstructured Chunks};
\node (llm) [box, below of=chunks] {5. LLM Context Window ("Lost in Middle")};

\draw [arrow] (query) -- (embed);
\draw [arrow] (embed) -- (vdb);
\draw [arrow] (vdb) -- (chunks);
\draw [arrow] (chunks) -- (llm);
\end{tikzpicture}
\caption{Standard RAG Architecture. The entire unstructured retrieval burden occurs linearly at query time, creating significant latency and semantic disconnection.}
\label{fig:rag_issues}
\end{figure}

Second, standard RAG fails at cross-system multi-hop reasoning. If an answer requires linking a Slack message to a Jira ticket, traditional RAG must either rely on the LLM's internal reasoning to bridge the chunks (assuming both were retrieved), or employ iterative, multi-step agentic loops which compound query-time latency exponentially.
""")

    # 3. NEW FILE: CCC ARCHITECTURE & Diagram
    with open(os.path.join(paper_dir, "02b_ccc_architecture.tex"), 'w', encoding='utf-8') as f:
        f.write(r"""
\section{Continuous Context Computation (CCC)}
\label{sec:ccc}

To resolve the query-time bottlenecks of RAG, we propose \textbf{Continuous Context Computation (CCC)}. CCC formally decouples context computation from inference computation.

\subsection{The CCC Algorithmic Framework}
Rather than treating retrieval as a reactionary search problem, CCC treats enterprise knowledge as a continuously flowing state machine. Data streams from disparate systems (Slack, Jira, Confluence) are ingested asynchronously. The CCC engine continuously extracts entities, resolves schemas, and computes relational edges in the background, maintaining a highly structured, temporally-aware Semantic Graph.

At query time, the system no longer performs a linear $O(N)$ scan over the entire corpus. Instead, it identifies the starting nodes within the pre-computed graph and traverses the explicitly maintained edges $E$. This reduces the retrieval complexity from a global $O(N)$ unstructured search to a localized $O(E)$ graph neighborhood traversal.

\begin{figure}[h]
\centering
\begin{tikzpicture}[
    node distance=1.5cm, auto, scale=0.8, transform shape,
    box/.style={rectangle, draw, fill=blue!10, text width=3.5cm, text centered, rounded corners, minimum height=1cm},
    widebox/.style={rectangle, draw, fill=green!10, text width=7.5cm, text centered, rounded corners, minimum height=1cm},
    arrow/.style={thick,->,>=stealth}
]
\node (data) [widebox] {Asynchronous Enterprise Data Streams};
\node (engine) [widebox, below of=data] {Continuous Context Engine (Offline Prep)};
\node (graph) [widebox, below of=engine] {Pre-computed Semantic Graph ($O(E)$)};

\node (query) [box, fill=yellow!20, right=0.5cm of engine] {User Query};
\node (llm) [box, fill=yellow!20, right=0.5cm of graph] {Instant LLM Response};

\draw [arrow] (data) -- (engine);
\draw [arrow] (engine) -- (graph);
\draw [arrow] (query) -- (graph);
\draw [arrow] (graph) -- (llm);
\end{tikzpicture}
\caption{The CCC Architecture. By computing and maintaining the semantic graph asynchronously, the online query avoids $O(N)$ scaling limits entirely.}
\label{fig:ccc_arch}
\end{figure}

By executing the heavy lifting of semantic alignment \textit{before} the user ever asks a question, CCC achieves flat latency scaling and near-perfect semantic provenance tracking.
""")

    # 4. FIX APPENDIX (Remove overflowing JSON, add detailed research text)
    with open(os.path.join(paper_dir, "10_appendix.tex"), 'w', encoding='utf-8') as f:
        f.write(r"""
\appendix
\section{Appendix: Methodological Constraints and Dataset Generation Algorithms}
\label{sec:appendix}

\subsection{Algorithmic Constraints of the Synthetic Corpus}
Rather than utilizing raw JSON schemas which often fail to convey the deep relational complexity of enterprise environments, we formalize the dataset generation logic used to create the 512,000 document corpus.

The data generator strictly enforces a scale-free network topology using the Barabási–Albert (BA) preferential attachment model. When a new document node $d_{new}$ is generated from a simulated platform (e.g., a GitHub commit), it attaches to existing entity nodes (e.g., an existing Developer or Jira Ticket) with a probability proportional to the target node's existing degree $k_i$:
\begin{equation}
P(d_{new} \rightarrow v_i) = \frac{k_i}{\sum_j k_j}
\end{equation}
This mathematically guarantees that our synthetic 512K corpus mimics the true "hub-and-spoke" nature of real-world enterprises, where core projects or central personnel become highly connected hubs.

\subsection{Resolution of Edge Decay}
To model the temporal nature of enterprise intelligence, every edge $e(u,v)$ generated in the benchmark contains a temporal weight decay function:
\begin{equation}
w(t) = w_0 \cdot e^{-\lambda (t - t_0)}
\end{equation}
This ensures that legacy context (e.g., a deprecated policy from 2021) naturally loses relevance compared to active, highly-traversed documentation, resolving the "context staleness" issue that plagues traditional caching mechanisms.
""")

    print("Paper successfully refined. Added TikZ architecture diagrams and deep CCC research domain analysis. Removed JSON overflow.")

if __name__ == "__main__":
    refine_paper()
