from api import get_friends
import time


def get_network(user_id, as_edgelist=True) -> list:
    friends = get_friends(user_id, '')
    links = []
    matrix = [[0] * len(friends) for _ in range(len(friends))]
    for i, friend in enumerate(friends):
        first_friends = []
        try:
            first_friends = get_friends(friend, '')
        except BaseException:
            pass
        time.sleep(0.34)
        for j, first_friend in enumerate(first_friends):
            for k, second_friend in enumerate(friends):
                if first_friend == second_friend:
                    links.append((i, k))
                    matrix[i][k] = 1

    return links if as_edgelist else matrix


def plot_graph(user_id: int) -> None:
    surnames = get_friends(user_id, 'last_name')
    vertices = [i['last_name'] for i in surnames]
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
