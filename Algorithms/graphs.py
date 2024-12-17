from collections import defaultdict, deque

class Graph:
    def __init__(self):
        self.graph = defaultdict(list)
        
    def add_edge(self, u, v):
        """Add edge from vertex u to vertex v"""
        self.graph[u].append(v)

    def dfs(self, start_vertex):
        """Depth First Search traversal from a given vertex"""
        # Set to keep track of visited vertices
        visited = set()
        result = []
        
        def dfs_helper(vertex):
            visited.add(vertex)
            result.append(vertex)
            
            # Recursively visit all adjacent vertices
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    dfs_helper(neighbor)
                    
        dfs_helper(start_vertex)
        return result

    def bfs(self, start_vertex):
        """Breadth First Search traversal from a given vertex"""
        # Set to keep track of visited vertices
        visited = set()
        # Queue for BFS
        queue = deque([start_vertex])
        visited.add(start_vertex)
        result = []
        
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            
            # Visit all adjacent vertices
            for neighbor in self.graph[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
        return result


def path_search(start, end, graph):
    ''' Finds any valid path from a to b in the provided graph.
    Each node is identified by an integer.
    The graph is directed : a->b does not imply b->a.
    Args:
        - graph is provided as an adjacency list, where graph[x] is
          a list of integers representing all nodes accessible from x.
        - node_a and node_b are integers representing the start and end.
    Return:
        A list of nodes representing any path from node_a to node_b.
        The path does not have to be the shortest one.
        If no path exists, return None.
    '''
    def dfs(current, end, graph, visited):
        if current == end:
            # Base case: reached the target node
            return [current]
        
        visited.add(current)  # Mark current node as visited
        
        for neighbor in graph.get(current, []):  # Safely get neighbors
            if neighbor not in visited:
                path = dfs(neighbor, end, graph, visited)
                if path:  # If a path is found, prepend current node
                    return [current] + path
        
        return None  # No path found from this node

    # Initialize a visited set and call DFS
    return dfs(start, end, graph, set())

# Example usage
if __name__ == "__main__":
    # Create a graph
    g = Graph()
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 3)
    
    print(g.graph.items())
    print("DFS starting from vertex 2:", g.dfs(2))
    print("BFS starting from vertex 2:", g.bfs(2))
