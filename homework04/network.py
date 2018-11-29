from api import get_friends
import igraph
import time


def get_network(user_id: int, as_edgelist: bool=True) -> list:
    users_ids = get_friends(user_id)['response']['items']
    edges = []
    matrix = [[0] * len(users_ids) for i in range(len(users_ids))]

    for friend1 in range(len(users_ids)):
        response = get_friends(users_ids[user1])
        friends = response
        for friend2 in range(friend + 1, len(users_ids)):
            if users_ids[friend2] in friends:
                if as_edgelist:
                    edges.append((friend1, friend2))
                else:
                    matrix[friend1][friend2] = 1
                    matrix[friend2][friend1] = 1
        time.sleep(0.4)

    if as_edgelist:
        return edges

    return matrix


def plot_graph(user_id: int) -> None:
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames['response']['items']]
    edges = get_network(user_id, True)

    g = igraph.Graph(vertex_attrs={"shape": "circle",
                                   "label": vertices,
                                   "size": 10},
                     edges=edges, directed=False)

    n = len(vertices)
    visual_style = {
        "vertex_size": 20,
        "edge_color": "gray",
        "layout": g.layout_fruchterman_reingold(
            maxiter=100000,
            area=n ** 2,
            repulserad=n ** 2)
    }

    g.simplify(multiple=True, loops=True)
    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)
    igraph.plot(g, **visual_style)