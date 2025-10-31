from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
import networkx as nx
import matplotlib.pyplot as plt
import copy
import random
import wikipedia
from wikipedia.exceptions import DisambiguationError
from loluwu import get_ultimate_summary
from summarizer import summarize_text
from Crawler_final import get_search_results


# Create your views here.
def search_page(request):
    return render(request, "search_page.html", context={})

def get_node(request: HttpResponse, q):
    d = request.GET.copy()
    d._mutable = True
    d["search"] = q
    request.POST = d
    return result_page(request)

def result_page(request):
    nodes = []
    query = request.POST["search"].lower()


    links = get_search_results(query=query)[:10]
    wiki = ""
    try:
        wiki = wikipedia.summary(query)
    except DisambiguationError as e:
        # wiki = wikipedia.search(query, results=5)
        wiki = ""
    except wikipedia.exceptions.PageError as e:
        pass


    _g = nx.read_gexf("final_graph.gexf")
    plt.clf()
    try:
        nodes = [query] + [n for n in _g.neighbors(query)] 
        g = nx.subgraph(_g, nodes)
        options = {
        'node_color': 'blue',
        'node_size': 2000,
        # 'width': 2,
        'arrowstyle': '-|>',
        'arrowsize': 12,
        # 'width': [1 * ds_graph[u][v][0]['weight'] for u, v in ds_graph.edges()],
        }
        
        
        nx.draw_kamada_kawai(g, with_labels=True, **options)
        pos = nx.kamada_kawai_layout(g)
        edge_labels = dict([((u,v,),d['weight'])
                    for u,v,d in g.edges(data=True)])

        nx.draw_networkx_edge_labels(
            g,
            pos, 
            edge_labels=edge_labels
        )

        nx.draw_networkx_nodes(g, pos, nodelist=[query], node_color="red", node_size=2000)

        plt.savefig(f"static/entrypoint/{query}.png")

    except nx.exception.NetworkXError as e:
        print(e)
        print("ERROR!!!")

    # context[query] = query


    p = get_ultimate_summary(query)
    print(p)

    # summary = summarize_text("HELLO HOW ARE YOU DOING")
    # print(summary)

    return render(request, "result_page.html", context={"query": query, "nodes": nodes, "links": links, "wiki": wiki, "summary": p})