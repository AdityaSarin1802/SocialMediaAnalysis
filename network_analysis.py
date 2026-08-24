"""
Network / Link Analysis Module
--------------------------------
Builds a directed graph from post mentions (who talks about whom),
then computes influence rankings and community clusters.

For production: swap the in-memory NetworkX graph for a Neo4j-backed
graph so it scales to millions of nodes/edges and supports live
Cypher queries from the dashboard.
"""

import networkx as nx


def build_interaction_graph(posts: list) -> nx.DiGraph:
    """Each mention creates a directed edge: author -> mentioned_user."""
    graph = nx.DiGraph()
    for post in posts:
        author = post["user_id"]
        graph.add_node(author, username=post.get("username", author))
        for mentioned in post.get("mentions", []):
            graph.add_node(mentioned)
            if graph.has_edge(author, mentioned):
                graph[author][mentioned]["weight"] += 1
            else:
                graph.add_edge(author, mentioned, weight=1)
    return graph


def top_influencers(graph: nx.DiGraph, top_n: int = 5) -> list:
    """
    Rank users by in-degree centrality (how often others mention them)
    combined with PageRank (accounts for indirect influence too).
    """
    if graph.number_of_nodes() == 0:
        return []

    in_degree = nx.in_degree_centrality(graph)
    pagerank = nx.pagerank(graph, weight="weight")

    ranked = sorted(
        graph.nodes(),
        key=lambda n: (pagerank.get(n, 0) + in_degree.get(n, 0)),
        reverse=True,
    )[:top_n]

    return [
        {
            "user_id": node,
            "username": graph.nodes[node].get("username", node),
            "in_degree_centrality": round(in_degree.get(node, 0), 3),
            "pagerank": round(pagerank.get(node, 0), 3),
        }
        for node in ranked
    ]


def detect_communities(graph: nx.DiGraph) -> list:
    """Group users into communities using greedy modularity (undirected view)."""
    if graph.number_of_nodes() < 2:
        return []

    undirected = graph.to_undirected()
    communities = nx.community.greedy_modularity_communities(undirected)
    return [sorted(list(c)) for c in communities]


def graph_summary(posts: list, top_n: int = 5) -> dict:
    graph = build_interaction_graph(posts)
    return {
        "num_users": graph.number_of_nodes(),
        "num_interactions": graph.number_of_edges(),
        "top_influencers": top_influencers(graph, top_n=top_n),
        "communities": detect_communities(graph),
    }