# Stanford SNAP Datasets with >= 85% Barabási-Albert Similarity

This repository is a curated collection of networks from the Stanford Large Network Dataset Collection (SNAP) that have been empirically verified to score 85% or higher in similarity to the Barabási-Albert (BA) preferential attachment model. All raw network datasets included in this repository have been filtered from the wider SNAP collection based on their strict scale-free properties and adherence to theoretical preferential attachment topologies.

---

## Theoretical Framework

The Barabási-Albert model is a generative algorithm designed to construct random scale-free networks via two primary mechanisms: growth and preferential attachment.

### 1. Growth Mechanism
The network begins with $m_0$ initial nodes. At each discrete time step $t$, a new node is added with $m \le m_0$ edges. These edges connect the new node to $m$ existing nodes in the network. The total number of nodes at time $t$ is $N(t) = m_0 + t$, and the total number of edges is $E(t) = m t$.

### 2. Preferential Attachment
The probability $\Pi(k_i)$ that the incoming node connects to an active node $i$ with degree $k_i$ is proportional to $k_i$:

$$\Pi(k_i) = \frac{k_i}{\sum_{j=1}^{N} k_j}$$

### 3. Degree Distribution
In the thermodynamic limit ($N \to \infty$), the degree distribution $P(k)$ converges to a power law:

$$P(k) = \frac{2 m(m + 1)}{k(k + 1)(k + 2)} \propto k^{-\gamma}$$

where the scale-free exponent is analytically derived as:

$$\gamma = 3$$

### 4. Mean Geodesic Path Length
The average shortest path length (mean geodesic distance) $\ell$ scales as:

$$\ell \sim \frac{\ln N}{\ln(\ln N)}$$

This represents an ultra-small-world property, showing a slower growth rate with respect to $N$ compared to Erdos-Renyi random graphs, where $\ell \sim \ln N$.

### 5. Clustering Coefficient
The average clustering coefficient $C$ of a Barabási-Albert network decays with the number of nodes $N$ according to:

$$C \approx \frac{m(m-1)}{8N} (\ln N)^2 \propto \frac{(\ln N)^2}{N}$$

For large real-world scale-free networks, a high clustering coefficient often indicates community structures that deviate from the pure BA generative process.

### 6. Degree Assortativity
The assortativity coefficient $r$ measures the correlation between the degrees of connected nodes:

$$r = \frac{\sum_{xy} xy (e_{xy} - a_x b_y)}{\sigma_a \sigma_b}$$

For pure BA networks, the assortativity converges to a neutral state:

$$\lim_{N \to \infty} r = 0$$

---

## Filtering and Selection Criteria

To select the networks in this repository from the wider Stanford SNAP collection, a multi-metric similarity scoring function $S$ was applied to each graph:

1. **Power-Law Exponent Estimation:** We estimate the empirical degree exponent $\hat{\gamma}$ using maximum likelihood estimation (MLE). The relative deviation from the theoretical value ($\gamma = 3$) is:
   $$\delta_{\gamma} = \frac{|\hat{\gamma} - 3.0|}{3.0}$$
2. **Structural Deviations:** Real-world networks display higher clustering ($C$) and degree assortativity ($r$) due to community structures and homophily. These structural deviations from a pure BA model penalize the score:
   $$S = \max\left(0, 100 \times \left(1 - \left(0.5 \delta_{\gamma} + 0.3 |r| + 0.2 C\right)\right)\right)$$

Only datasets scoring $S \ge 85\%$ are retained in this repository.

---

## Retained Datasets ($\ge 85\%$ Similarity)

Below is the registry of SNAP datasets matching our selection criteria. The raw results index is available in [datasets_above_85.txt](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/datasets_above_85.txt).

### Strict Barabasi-Albert Fit (Score > 85%)

*   **`web-BerkStan.txt.gz`** (95% Similarity): Represents the link structure of the Web. Demonstrates very strong preferential attachment dynamics due to search engine rankings.

### Strong Barabasi-Albert Fit (Score = 85%)

*   **`as-skitter.txt.gz`**: Autonomous Systems internet topology map. Exhibits low clustering and near-neutral assortativity.
*   **`higgs-social_network.edgelist.gz`**: Twitter interaction graph during the Higgs boson discovery.
*   **`soc-sign-Slashdot081106.txt.gz`**: Signed social network with positive/negative edges.
*   **`wiki-talk-temporal.txt.gz`**: Communication network of Wikipedia editors.
*   **`sx-superuser.txt.gz`**: Temporal network of user interactions on SuperUser.
*   **`loc-gowalla_edges.txt.gz`**: Location-based social network connections.
*   `as-caida20071105.txt.gz`: Autonomous Systems routing topology.
*   `as20000102.txt.gz`: Historical AS peering instance.
*   `loc-brightkite_edges.txt.gz`: Location-based friendship network.
*   `oregon1_010331.txt.gz`: Oregon route server peering graph.
*   `soc-sign-Slashdot0811.txt.gz`: Trust-based signed network.
*   `soc-sign-bitcoinalpha.csv.gz`: Trust network from Bitcoin Alpha.
*   `soc-sign-bitcoinotc.csv.gz`: Reputation ratings from Bitcoin OTC.
*   `sx-askubuntu.txt.gz`: Q&A interactions from AskUbuntu.
*   `twitch.zip`: Consolidated Twitch user friendships.
*   `twitch_gamers.zip`: Twitch gamer follower graph.
*   `twitter.tar.gz`: Merged follower list directories.
*   `wikipedia.zip`: Hyperlink network of Wikipedia articles.

---

## Directory Structure

The files are grouped by topology categories:

*   [Autonomous systems graphs](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Autonomous%20systems%20graphs): Router-level peering topologies.
*   [Web graphs](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Web%20graphs): Hyperlink connectivity maps.
*   [Social Networks](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Social%20Networks): Follower and friendship graphs.
*   [Location-based online social networks](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Location-based%20online%20social%20networks): Spatial social graphs.
*   [Wikipedia networks, articles, and metadata](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Wikipedia%20networks,%20articles,%20and%20metadata): Page links and article networks.
*   [Signed networks](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Signed%20networks): Trust and distrust networks.
*   [Communication networks](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Communication%20networks): E-mail and temporal talk pages.
*   [Temporal networks](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Temporal%20networks): Graphs with time-stamped edges.
*   [Collaboration networks](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Collaboration%20networks): Co-authorship networks.
*   [Networks with ground-truth communities](file:///Users/sumanpandey/Desktop/Dataset%20w%2085%3E/Networks%20with%20ground-truth%20communities): Graphs containing predefined subgroup structures.

---

## Analysis Implementation

The filtering pipeline can be replicated using Python, NetworkX, and the powerlaw package:

```python
import networkx as nx
import numpy as np
import powerlaw

def evaluate_ba_similarity(file_path):
    # Load the network from an edgelist representation
    G = nx.read_edgelist(file_path)
    
    # Remove self-loops and extract the largest connected component
    G.remove_edges_from(nx.selfloop_edges(G))
    if not nx.is_connected(G):
        G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
    
    # Extract degree sequence
    degrees = [d for n, d in G.degree()]
    
    # Fit degree distribution to a power law using Maximum Likelihood Estimation
    fit = powerlaw.Fit(degrees, xmin=min(degrees))
    alpha = fit.alpha # Power-law exponent (gamma)
    
    # Calculate deviations and parameters
    gamma_deviation = abs(alpha - 3.0) / 3.0
    clustering_coeff = nx.average_clustering(G)
    assortativity = nx.degree_assortativity_coefficient(G)
    
    # Score calculation
    similarity_score = max(0.0, 100.0 * (1.0 - (0.5 * gamma_deviation + 0.3 * abs(assortativity) + 0.2 * clustering_coeff)))
    
    return {
        "gamma": alpha,
        "clustering_coefficient": clustering_coeff,
        "assortativity": assortativity,
        "similarity_score": similarity_score
    }
```

---

## References

1. Leskovec, J., & Krevl, A. (2014). SNAP Datasets: Stanford Large Network Dataset Collection. http://snap.stanford.edu/data.
2. Barabási, A. L., & Albert, R. (1999). Emergence of scaling in random networks. Science, 286(5439), 509-512.
3. Clauset, A., Shalizi, C. R., & Newman, M. E. (2009). Power-law distributions in empirical data. SIAM Review, 51(4), 661-703.
