import networkx as nx
import matplotlib.pyplot as plt

class NetworkGraph:

    def __init__(self):
        self.graph = nx.MultiDiGraph(directed=True)
    
    def add_nodes(self, golden_token, silver_token, weight):
        self.graph.add_node(golden_token)
        self.graph.add_node(silver_token)
        self.graph.add_edge(golden_token, silver_token, weight=weight)
    

    def print_graph(self):
        # print(self.graph['Sachin']["Abhishek"][0]['weight'])
        options = {
            'node_color': 'blue',
            'node_size': 250,
            'width': 2,
            'arrowstyle': '-|>',
            'arrowsize': 12,
            'width': [1 * self.graph[u][v][0]['weight'] for u, v in self.graph.edges()],

        }
        nx.draw_circular(self.graph, with_labels=True, **options)
        pos = nx.circular_layout(self.graph)
        edge_labels = dict([((u,v,),d['weight'])
                 for u,v,d in self.graph.edges(data=True)])

        nx.draw_networkx_edge_labels(
            self.graph,
            pos, 
            edge_labels=edge_labels
        )

        plt.savefig("hello.png")




if __name__ == "__main__":
    ng = NetworkGraph()

    ng.add_nodes("Sachin", "Abhishek", 1.4)
    ng.add_nodes("Tushar", "Hardik", 2)
    ng.add_nodes("Sachin", "Hardik", 4)

    ng.print_graph()