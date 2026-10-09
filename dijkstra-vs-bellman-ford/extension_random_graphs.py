import heapq
import itertools
import random

VERTICES = ['s', 'A', 'B', 't']
SOURCE = 's'
P_CONNECT = 0.7
Q_NEGATIVE_FIRST = 0.3


def generate_random_graph(vertices=VERTICES, p=P_CONNECT, q=Q_NEGATIVE_FIRST):
    """Κατασκευάζει τυχαίο γράφο όπως περιγράφει η εκφώνηση: για κάθε αδιάτακτο
    ζεύγος κορυφών, με πιθανότητα p υπάρχει σύνδεση (και οι δύο κατευθύνσεις),
    και με πιθανότητα q η πρώτη κατεύθυνση παίρνει βάρος -1 (η αντίθετη +1),
    διαφορετικά η πρώτη παίρνει +1 (η αντίθετη -1)."""
    graph = {v: {} for v in vertices}
    for u, v in itertools.combinations(vertices, 2):
        if random.random() < p:
            if random.random() < q:
                graph[u][v], graph[v][u] = -1, 1
            else:
                graph[u][v], graph[v][u] = 1, -1
    return graph


def has_negative_edge(graph):
    return any(w < 0 for neighbors in graph.values() for w in neighbors.values())


def dijkstra(graph, source):
    """Μηχανική (τυπική) εκτέλεση Dijkstra: οριστικοποιεί άπληστα την κορυφή με
    τη μικρότερη προσωρινή απόσταση και δεν την επανεξετάζει ποτέ ξανά -- ακόμη
    κι αν υπάρχουν αρνητικά βάρη που θα την έκαναν λανθασμένη."""
    dist = {v: float('inf') for v in graph}
    dist[source] = 0
    visited = set()
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        for v, w in graph[u].items():
            if v in visited:
                continue
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist


def bellman_ford(graph, source):
    """Σωστός αλγόριθμος για γράφους με αρνητικά βάρη. Επιστρέφει τις αποστάσεις
    (με -inf στις κορυφές που επηρεάζονται από προσβάσιμο αρνητικό κύκλο) και
    το αν εντοπίστηκε αρνητικός κύκλος."""
    vertices = list(graph.keys())
    dist = {v: float('inf') for v in vertices}
    dist[source] = 0
    edges = [(u, v, w) for u in graph for v, w in graph[u].items()]

    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    affected = {v for u, v, w in edges if dist[u] != float('inf') and dist[u] + w < dist[v]}

    has_negative_cycle = bool(affected)
    if has_negative_cycle:
        stack = list(affected)
        neg_inf_nodes = set(affected)
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in neg_inf_nodes:
                    neg_inf_nodes.add(v)
                    stack.append(v)
        for v in neg_inf_nodes:
            dist[v] = float('-inf')

    return dist, has_negative_cycle


def dijkstra_matches_bellman_ford(dijkstra_dist, bf_dist):
    return all(dijkstra_dist.get(v, float('inf')) == bf_dist[v] for v in bf_dist)


def run_experiment(trials=100_000, seed=None):
    if seed is not None:
        random.seed(seed)

    stats = {
        "trials": trials,
        "has_negative_edge": 0,
        "has_negative_cycle": 0,
        "dijkstra_correct": 0,
        "dijkstra_incorrect": 0,
    }

    for _ in range(trials):
        graph = generate_random_graph()

        if has_negative_edge(graph):
            stats["has_negative_edge"] += 1

        bf_dist, has_neg_cycle = bellman_ford(graph, SOURCE)
        if has_neg_cycle:
            stats["has_negative_cycle"] += 1

        dij_dist = dijkstra(graph, SOURCE)
        if dijkstra_matches_bellman_ford(dij_dist, bf_dist):
            stats["dijkstra_correct"] += 1
        else:
            stats["dijkstra_incorrect"] += 1

    return stats


def print_report(stats):
    n = stats["trials"]
    print(f"Trials: {n}")
    print(f"  Graphs with at least one negative edge: {stats['has_negative_edge']} "
          f"({100 * stats['has_negative_edge'] / n:.2f}%)")
    print(f"  Graphs with a negative cycle reachable from s: {stats['has_negative_cycle']} "
          f"({100 * stats['has_negative_cycle'] / n:.2f}%)")
    print(f"  Dijkstra correct (matches Bellman-Ford): {stats['dijkstra_correct']} "
          f"({100 * stats['dijkstra_correct'] / n:.2f}%)")
    print(f"  Dijkstra incorrect: {stats['dijkstra_incorrect']} "
          f"({100 * stats['dijkstra_incorrect'] / n:.2f}%)")


if __name__ == "__main__":
    # Ελεγχος ορθότητας στο συγκεκριμένο στιγμιότυπο της άσκησης (ερωτήματα 5-8).
    instance_graph = {
        's': {'A': 1, 'B': -1},
        'A': {'s': -1, 'B': 1, 't': 1},
        'B': {'s': 1, 'A': -1, 't': 1},
        't': {'A': -1, 'B': -1},
    }
    dij = dijkstra(instance_graph, 's')
    bf, neg_cycle = bellman_ford(instance_graph, 's')
    assert dij == {'s': 0, 'A': -2, 'B': -1, 't': -1}, dij
    assert neg_cycle is True
    assert all(bf[v] == float('-inf') for v in ['s', 'A', 'B', 't'])
    print("Sanity check on the exercise's specific instance: OK")
    print(f"  Dijkstra: {dij}")
    print(f"  Bellman-Ford: {bf}, negative cycle: {neg_cycle}")
    print()

    # Πείραμα σε πολλούς τυχαίους γράφους.
    stats = run_experiment(trials=100_000, seed=42)
    print_report(stats)
