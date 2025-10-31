from graph_irt import NetworkGraph
import networkx as nx
from networkx.classes import Graph
from networkx.exception import NodeNotFound
from pathlib import Path
import os
from math import log

class PatternModel:
    SEPERATION_COEFFICIENT = 100
    ACTIVATION_THRESHOLD = 0.2

    def __init__(self, tokens: list[str], corpus_path: Path):
        self.sg = NetworkGraph()
        self.tokens = tokens
        self.corpus_path = corpus_path
        
        self.load_tokens()

        self.current_model = self.sg.print_graph
    
    def load_tokens(self):
        for token in self.tokens:
            self.sg.graph.add_node(token)

    
    def write_graph(self):
        nx.write_gexf(G, "final.gexf")
    
    def read_graph(self, path):
        self.sg = nx.read_gexf(path) 

    def initial_pattern_learning(self):
        os.chdir(self.corpus_path)
        p = os.listdir()
        
        documents = []
        i = 1
        for document in p:
            if not document.endswith(".txt"):
                continue

            print(f"document processing done: {i / len(p) * 100}%")
            i += 1
            with open(document, "r") as f:
                l = f.read()
            
            ##### PREPROCESSING

            l = l.split()

            remove_list = [",", ".",  "-", ":"]
            doc = []

            for word in l:
                if word not in remove_list and not word.isnumeric():
                    doc.append(word.lower())


            bi_words = [f"{doc[i]} {doc[i+1]}" for i in range(len(doc) -1)]
            tri_words = [f"{doc[i]} {doc[i+1]} {doc[i+2]}" for i in range(len(doc) -2)]
            doc += bi_words + tri_words
            documents.append(doc)
        
        print(f"document processing done: 100%")
        ##################

        docs = []
        for d in documents:
            docs += d
        # print(doc)

        ##### TF-IDF 
        tf_idf = {}
        for token in self.tokens:
            count = 0
            for doc in docs:
                if token in doc:
                    count += 1
            
            tf_idf[token] = log(len(docs)/(1+count))
        ############

        for golden_token in self.tokens:
            doc = docs.copy()
            for silver_token in self.tokens:
                
                if silver_token == golden_token:
                    pass
                else:
                    weight_list = []
                    while golden_token in doc and silver_token in doc:
                        golden_token_position = doc.index(golden_token)
                        silver_token_position = doc.index(silver_token)

                        doc.remove(silver_token)

                        diff = golden_token_position - silver_token_position
                        if abs(diff) > self.SEPERATION_COEFFICIENT: continue
                        
                        weight_list.append(abs(1/diff))
                    
                    if len(weight_list) == 0: continue
                    weight = (sum(weight_list) / len(weight_list))
                    weight *= 100
                    # if weight < 0:
                    #     weight = log(abs(weight), 10)      
                    #     if abs(weight) < 0.2:
                    #         continue         
                    #     weight = round(weight, 2)
                    #     self.sg.graph.add_node(golden_token)
                    #     self.sg.graph.add_node(silver_token)
                    #     self.sg.graph.add_edge(silver_token, golden_token, weight=weight)
                    #     continue
                    
                    weight /= tf_idf[golden_token]
                    weight = log(abs(weight), 10)

                    if abs(weight) < self.ACTIVATION_THRESHOLD:
                        continue         
                    weight = abs(round(weight, 2))
                   
                    self.sg.graph.add_node(golden_token)
                    self.sg.graph.add_node(silver_token)
                    self.sg.graph.add_edge(silver_token, golden_token, weight=weight)



        os.chdir("..")

def fetch_sub_graph(G: Graph, sub_nodes: list):
    return G.subgraph(sub_nodes)


def find_path_between(G: Graph, source, target):
    try:
        shortest_path = nx.shortest_path(G, source=source, target=target)
    except NodeNotFound as e:
        return False
    return shortest_path

############ OPTIONAL BUT COOL ############################################
def find_path_with_known_nodes(G: Graph, source_list: list, target: str): 
    paths = []                                                            
    for source in source_list:                                            
        path = find_path_between(G, source, target)                       
        if not path or path == None:                                      
            continue

        paths.append(path)

    # merge
    final = []
    for path in paths:
        final += path
    return paths
###########################################################################

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from random import random
    from random import seed
    from math import log
    seed("Sachin")
    # python

    python_tokens = [
        "python",  "variable", "lists", "tuple", "dictonary", "data types",
        "loops", "for loop", "while loop", "control statements", "if", "else", "elif",
        "functions", "def", "condional statements", "slicing", "class", "sorting",
        "data structure", "stack", "queue"
    ]
    python_graph = nx.MultiDiGraph(directed=True)
    python_weights = []
    for token in python_tokens:
        python_graph.add_node(token)
        for ttoken in python_tokens:
            if ttoken == token:
                continue
            python_weights.append([token, ttoken, round(1/log(10*random(), 2), 2)])

    options = {
    'node_color': 'blue',
    'node_size': 250,
    # 'width': 2,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    # 'width': [1 * python_graph[u][v][0]['weight'] for u, v in python_graph.edges()],
    }

    for weights in python_weights:
        print(weights[2])
        if weights[2] < 0.5:
            continue
        python_graph.add_edge(weights[0], weights[1], weight=weights[2])

    # nx.draw_kamada_kawai(python_graph, with_labels=True, **options)
    # pos = nx.kamada_kawai_layout(python_graph)
    # edge_labels = dict([((u,v,),d['weight'])
    #             for u,v,d in python_graph.edges(data=True)])

    # nx.draw_networkx_edge_labels(
    #     python_graph,
    #     pos, 
    #     edge_labels=edge_labels
    # )
    # nx.write_gexf(python_graph, "python_graph.gexf")

    # plt.savefig("python_graph.png")


    # DS
    ds_tokens = [
        "data structure", "data", "singly", "doubly", "stack", "queue", "array",
        "lists", "linked", "linear", "graph", "binary", "heap", "binary tree",
        "quick sort", "binary search", "hash tables", "merging"
    ]

    ds_graph = nx.MultiDiGraph(directed=True)
    ds_weights = []
    for token in ds_tokens:
        ds_graph.add_node(token)
        for ttoken in ds_tokens:
            if ttoken == token:
                continue
            ds_weights.append([token, ttoken, round(1/log(10*random(), 2), 2)])

    options = {
    'node_color': 'blue',
    'node_size': 250,
    # 'width': 2,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    # 'width': [1 * ds_graph[u][v][0]['weight'] for u, v in ds_graph.edges()],
    }
    
    # print(ds_weights)
    for weights in ds_weights:
        if weights[2] < 0.5:
            continue
        print(weights[2])
        ds_graph.add_edge(weights[0], weights[1], weight=weights[2])

    print("done")
    # nx.draw_kamada_kawai(ds_graph, with_labels=True, **options)
    # pos = nx.kamada_kawai_layout(ds_graph)
    # edge_labels = dict([((u,v,),d['weight'])
    #             for u,v,d in ds_graph.edges(data=True)])

    # nx.draw_networkx_edge_labels(
    #     ds_graph,
    #     pos, 
    #     edge_labels=edge_labels
    # )
    # nx.write_gexf(ds_graph, "ds_graph.gexf")
    # plt.savefig("ds_graph.png")


    # # Algorithm
    al_tokens = [
        "sorting", "searching", "selection sort", "bubble sort", "insertion sort",
        "quick sort", "linear search", "binary search", "merging", "traversal"
    ]

    al_graph = nx.MultiDiGraph(directed=True)
    al_weights = []
    for token in al_tokens:
        al_graph.add_node(token)
        for ttoken in al_tokens:
            if ttoken == token:
                continue
            al_weights.append([token, ttoken, round(1/log(10*random(), 2), 2)])

    options = {
    'node_color': 'blue',
    'node_size': 250,
    # 'width': 2,
    'arrowstyle': '-|>',
    'arrowsize': 12,
    # 'width': [1 * ds_graph[u][v][0]['weight'] for u, v in ds_graph.edges()],
    }
    
    # print(ds_weights)
    for weights in al_weights:
        if weights[2] < 0.5:
            continue
        print(weights[2])
        al_graph.add_edge(weights[0], weights[1], weight=weights[2])

    print("done")
    # nx.draw_kamada_kawai(al_graph, with_labels=True, **options)
    # pos = nx.kamada_kawai_layout(al_graph)
    # edge_labels = dict([((u,v,),d['weight'])
    #             for u,v,d in al_graph.edges(data=True)])

    # nx.draw_networkx_edge_labels(
    #     al_graph,
    #     pos, 
    #     edge_labels=edge_labels
    # )

    # plt.savefig("al_graph.png")
    # nx.write_gexf(al_graph, "al_graph.gexf")

    # exit()

    # # Graphs making

    final_graph = nx.MultiDiGraph(directed=True)

    graphs = [ds_graph, python_graph, al_graph]

    final_graph = nx.compose_all(graphs)

    nx.draw_kamada_kawai(final_graph, with_labels=True, **options, node_size=1500, node_color="skyblue", node_shape="s", alpha=0.5, linewidths=40)
    pos = nx.kamada_kawai_layout(final_graph)
    edge_labels = dict([((u,v,),d['weight'])
                for u,v,d in final_graph.edges(data=True)])

    nx.draw_networkx_edge_labels(
        final_graph,
        pos, 
        edge_labels=edge_labels
    )

    plt.savefig("final_graph.png")
    nx.write_gexf(final_graph, "final_graph.gexf")

    # token_graphs = [python_tokens, ds_tokens, algorithms_token]

    # for tokens in token_graphs:
    #     g = nx.MultiDiGraph(directed=True)
        
    #     for token in tokens:
    #         g.add_node(token)
        
    #     graphs.append(g)
    


    # for graph in graphs:
    #     final_graph = nx.compose(final_graph, graph)

    # nx.draw_kamada_kawai(final_graph, with_labels=True)
    # plt.savefig("hiii.png")
    









    # paths = [
    #     ["algebra", "variable", "numbers", "trignometry"],
    #     ["sin", "variable", "trignometry"],
    #     ""
    # ]
    # G = nx.watts_strogatz_graph(30, 5, 0.1, seed=1234)
    # path_between = find_path_between(G, 18, 2)

    
    # sg = fetch_sub_graph(G, path_between)
    # nx.draw_kamada_kawai(sg, with_labels=True)

    # plt.savefig("BEB_sub.png")
    # print(sg)
    # pass

    # import time

    # for i in range(100, 2000, 100):
        # print("Seperation Threshold: ", i)
        # tokens = ["regression", "correlation", "vif", "random variable", "independent variable", "dependent variable", "assumption", "assumptions", "variable"]
        
        # # tokens = ["machine learning", "data science", "artificial intelligence", "regression", "classification", "correlation"]
        # pm = PatternModel(tokens, Path("Regression Documents"))
        # pm.SEPERATION_COEFFICIENT = i
        # pm.initial_pattern_learning()
        # pm.current_model()
        # time.sleep(1)
        # print(nx.shortest_path(pm.sg.graph, source="regression", target="linear regression"))
 
        # print("Graph 1 Done")
        
        # tokens = ["asif", "correlation", "matrix", "pca", "principal component analysis", "rank", "diagonal matrix", "eigen vector", "eigen values", "vectors", "algebra", "transpose", "symmetric"] 
        # pm2 = PatternModel(tokens, Path("Linear Algebra documents"))
        # pm2.initial_pattern_learning()
        # pm.current_model()

        # print("Graph 2 done")
        # print("Composing both graph")

        # F = NetworkGraph()
        # F.graph = nx.compose(pm.sg.graph, pm2.sg.graph)
        # F.print_graph()

        # print(nx.shortest_path(pm.sg.graph, source="regression", target="random variable"))
    # print(nx.shortest_path(pm.sg.graph, source="data science", target="classification"))

