import time
import random
import heapq
import random


def generate_nodes(num_nodes):
    time.sleep(0.1)
    return [chr(ord('A') + i) for i in range(num_nodes)]


def generate_random_edges(nodes, num_edges):
    edges = set()
    time.sleep(0.2)
    while len(edges) < num_edges:
        node1 = random.choice(nodes)
        node2 = random.choice(nodes)

        if node1 != node2:
            edges.add((node1, node2))

    return list(edges)


def generate_random_weights(edges):
    weights = {}
    for edge in edges:
        weights[edge] = random.randint(1, 10)
    return weights


def generate_random_graph(num_nodes, num_edges):
    nodes = generate_nodes(num_nodes)
    edges = generate_random_edges(nodes, num_edges)
    weights = generate_random_weights(edges)

    graph = {node: {} for node in nodes}

    for edge in edges:
        node1, node2 = edge
        weight = weights[edge]
        graph[node1][node2] = weight
        graph[node2][node1] = weight

    return graph


def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    predecessors = {node: None for node in graph}
    distances[start] = 0

    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        time.sleep(0.5)
        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances, predecessors


def print_shortest_paths(start_node, distances, predecessors):
    time.sleep(0.5)
    for node, distance in distances.items():
        print(f"Shortest distance from {start_node} to {node}: {distance}")


def print_shortest_path(start_node, target_node, predecessors):
    if target_node in predecessors:
        path = []
        while target_node:
            path.insert(0, target_node)
            target_node = predecessors[target_node]
        print(f"Shortest path from {start_node} to {path[-1]}: {' -> '.join(path)}")
    else:
        print(f"No path from {start_node} to {target_node}")


# Test Dijkstra's algorithm with a random graph
num_nodes = 26
num_edges = 260  # Adjust as needed for your performance testing

graph = generate_random_graph(num_nodes, num_edges)

start_node = 'A'
distances, predecessors = dijkstra(graph, start_node)

print_shortest_paths(start_node, distances, predecessors)

target_node = 'Z'  # Change this to a valid node name
print_shortest_path(start_node, target_node, predecessors)
