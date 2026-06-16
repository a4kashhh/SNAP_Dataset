import os
import gzip
import zipfile
import tarfile
import tempfile
import networkx as nx
import numpy as np
import powerlaw

def extract_and_load_graph(file_path):
    """
    Extracts compressed files and loads them into a NetworkX Graph.
    Supports .gz, .zip, and .tar.gz files.
    """
    _, ext = os.path.splitext(file_path)
    
    # Handle .gz files
    if file_path.endswith('.gz') and not file_path.endswith('.tar.gz'):
        with gzip.open(file_path, 'rt') as f:
            return nx.read_edgelist(f)
            
    # Handle .zip files
    elif ext == '.zip':
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            # Get list of files in zip
            file_names = zip_ref.namelist()
            # Filter out directories and metadata files
            valid_files = [f for f in file_names if not f.startswith('__MACOSX') and f.endswith(('.txt', '.csv', '.edgelist'))]
            if not valid_files:
                raise ValueError("No valid graph files found inside zip archive")
            
            with tempfile.TemporaryDirectory() as tmpdir:
                zip_ref.extract(valid_files[0], path=tmpdir)
                extracted_path = os.path.join(tmpdir, valid_files[0])
                return nx.read_edgelist(extracted_path)
                
    # Handle .tar.gz files
    elif file_path.endswith('.tar.gz'):
        with tarfile.open(file_path, 'r:gz') as tar_ref:
            valid_members = [m for m in tar_ref.getmembers() if m.isfile() and m.name.endswith(('.txt', '.csv', '.edgelist'))]
            if not valid_members:
                raise ValueError("No valid graph files found inside tar archive")
            
            with tempfile.TemporaryDirectory() as tmpdir:
                tar_ref.extract(valid_members[0], path=tmpdir)
                extracted_path = os.path.join(tmpdir, valid_members[0])
                return nx.read_edgelist(extracted_path)
                
    # Standard uncompressed files
    else:
        return nx.read_edgelist(file_path)

def evaluate_ba_similarity(G):
    """
    Evaluates the structural similarity of the graph G to the Barabási-Albert model.
    Returns the similarity score, power-law exponent, clustering coefficient, and assortativity.
    """
    # Remove self-loops
    G.remove_edges_from(nx.selfloop_edges(G))
    
    # If graph is disconnected, extract the largest connected component
    if not nx.is_connected(G):
        largest_cc = max(nx.connected_components(G), key=len)
        G = G.subgraph(largest_cc).copy()
        
    # Extract degree sequence
    degrees = [d for n, d in G.degree()]
    if not degrees or max(degrees) == 0:
        return 0.0, 0.0, 0.0, 0.0
        
    # Fit degree distribution to a power-law distribution
    # xmin is determined automatically using MLE
    try:
        fit = powerlaw.Fit(degrees, xmin=min(degrees), verbose=False)
        alpha = fit.alpha
    except Exception:
        # Fallback if fit fails
        alpha = 0.0
        
    # Calculate topological metrics
    gamma_deviation = abs(alpha - 3.0) / 3.0
    clustering_coeff = nx.average_clustering(G)
    
    try:
        assortativity = nx.degree_assortativity_coefficient(G)
        if np.isnan(assortativity):
            assortativity = 0.0
    except Exception:
        assortativity = 0.0
        
    # Compute similarity score based on normalized deviations
    # High assortativity and high clustering indicate deviations from pure BA preferential attachment
    similarity_score = max(0.0, 100.0 * (1.0 - (0.5 * gamma_deviation + 0.3 * abs(assortativity) + 0.2 * clustering_coeff)))
    
    return similarity_score, alpha, clustering_coeff, assortativity

def scan_repository():
    """
    Scans the repository categories, runs BA similarity checks on all files, and prints results.
    """
    categories = [
        "Autonomous systems graphs",
        "Web graphs",
        "Social Networks",
        "Memetracker and Twitter",
        "Location-based online social networks",
        "Wikipedia networks, articles, and metadata",
        "Signed networks",
        "Communication networks",
        "Temporal networks",
        "Collaboration networks",
        "Networks with ground-truth communities"
    ]
    
    print("=" * 70)
    print("      STANFORD SNAP DATASET: BARABASI-ALBERT SIMILARITY RUNNER")
    print("=" * 70)
    
    results = []
    
    for category in categories:
        category_path = category
        if not os.path.exists(category_path):
            continue
            
        print(f"\n📂 Scanning Category: {category}")
        for file in os.listdir(category_path):
            if file == ".DS_Store" or file.startswith("CiscoSecureWorkload"):
                continue
                
            file_path = os.path.join(category_path, file)
            if os.path.isfile(file_path):
                print(f"  📄 Processing {file}...", end="", flush=True)
                try:
                    G = extract_and_load_graph(file_path)
                    score, gamma, cc, assort = evaluate_ba_similarity(G)
                    print(f" Done! Score: {score:.1f}% (γ={gamma:.2f}, C={cc:.3f}, r={assort:.3f})")
                    results.append((file, category, score, gamma, cc, assort))
                except Exception as e:
                    print(f" Failed! Error: {str(e)}")
                    
    # Sort and display results
    print("\n" + "=" * 70)
    print("                      FINAL RESULTS (Sorted by Score)")
    print("=" * 70)
    results.sort(key=lambda x: x[2], reverse=True)
    for r in results:
        print(f"{r[0]:<35} | {r[1]:<30} | {r[2]:>5.1f}%")
    print("=" * 70)

if __name__ == "__main__":
    scan_repository()
