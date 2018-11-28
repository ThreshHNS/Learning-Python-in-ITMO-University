from api import get_friends
import igraph
import time
from typing import Union, List, Tuple

def get_network(user_id: list, as_edgelist: bool=True) -> Union[List[List[int]], List[Tuple[int, int]]]:

    users_ids = get_friends(user_id)['response']['items']
    edges = []
    matrix = [[0] * len(users_ids) for _ in range(len(users_ids))]

    for i in range(len(users_ids)):
        time.sleep(0.33333334)
        response = get_friends(users_ids[i])
        if response.get('error'):
            continue
        friends = response['response']['items']

        for j in range(i + 1, len(users_ids)):
            if users_ids[j] in friends:
                if as_edgelist:
                    edges.append((i, j))
                else:
                    matrix[i][j] = 1

    if as_edgelist:
        return edges
    else:
        return matrix


def plot_graph(user_id: list) -> None:

    surnames = get_friends(user_id, 'last_name')
    vertices = [surnames['response']['items'][i]['last_name']
                for i in range(len(surnames['response']['items']))]
    edges = get_network(user_id)
    g = Graph(vertex_attrs={"shape": "circle",
                            "label": vertices,
                            "size": 10},
              edges=edges, directed=False)

    N = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "bbox": (2000, 2000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "edge_color": "gray",
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=N ** 2,
            repulserad=N ** 2)
    }

    communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    g.simplify(multiple=True, loops=True)

    plot(g, **visual_style)
