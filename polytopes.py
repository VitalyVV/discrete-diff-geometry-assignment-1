import numpy as np
import math


class Variety():
    def __init__(self, faces):
        self.faces = faces
        vertices = set(i for f in faces for i in f)
        self.n = max(vertices) + 1
        assert set(range(self.n)) == vertices
        for f in faces:
            assert len(f) == 3

    @property
    def num_vertices(self):
        return self.n

    def check(self):
        def is_pair_halfedges(edge1, edge2):
            return edge1[0]==edge2[1] and edge2[0]==edge1[1]

        edges, n_edges = self.edge_info()
        traversed_vertices = self.bfs(edges, edges[0][0])
        vertices = np.unique(self.faces)
        pairs = 0

        for i in range(len(edges)):
            for j in range(len(edges)):
                if is_pair_halfedges(edges[i], edges[j]):
                    pairs += 1

        is_connected = pairs/2 == n_edges
        for i in range(len(self.faces)):
            for j in range(len(self.faces)):
                if i != j:
                    if set(self.faces[i])==set(self.faces[j]):
                        is_connected = False
                        break

        return is_connected and set(traversed_vertices) == set(vertices)

    def Euler(self):
        # Formula missing edges, so find it first
        n_edges = self.edge_info()[1]
        # Using Vertices - edges + faces formula find Euler characteristics
        return self.num_vertices - n_edges + len(self.faces)

    def d_0(self, func):
        return lambda x, y: func(y) - func(x)

    def d_1(self, func):
        return lambda x, y, z: func(x, y) + func(y, z) + func(z, x)

    def check_form(self, k, func):
        if k == 1:
            x, y = 1, 1
            return func(x,y)==-func(x,y)
        else:
            x,y,z = 1,1,1
            return func(x,y,z)==func(x,y,z)

    def wedge(self, k1, k2, f1, f2):
        def bases(k):
            return math.factorial(3) / (math.factorial(k) * math.factorial(3 - k))

        if k1 == 0 and k2 == 0:
            return lambda x: f1(x) * f2(x)
        if k1 == 0 and k2 == 1:
            return lambda x, y: 1/2 * (f1(x) * f2(x, y) + f1(y) * f2(x, y)) 
        if k1 == 0 and k2 == 2:
            return lambda x, y, z: 1/3 * (f1(x) * f2(x, y, z) + f1(y) * f2(x, y, z) + f1(z) * f2(x, y, z))
        if k1 == 1 and k2 == 1:
            return lambda x, y, z: 1/6 * (f1(x, y) * f2(y, z) - f1(y, z) * f2(x, y) + 
                                          f1(y, z) * f2(z, x) - f1(z, x) * f2(y, z) +
                                          f1(z, x) * f2(x, y) - f1(x, y) * f2(z, x) )
        if k1 == 1 and k2 == 2:
            return lambda x, y, z: 0



    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
    def bfs(self, edges, v_0):
        def get_adjaced_vertex(v, edge):
            return edge[0] if v==edge[1] else edge[1]

        queue = [v_0]
        marked = [v_0]
        traversed = [v_0]
        while len(queue) != 0:
            t = queue[0]
            del queue[0]
            if not t in marked:
                marked.append(t)
                traversed.append(t)
            adjacent_edges = [edge for edge in edges if t in edge]
            for edge in adjacent_edges:
                o = get_adjaced_vertex(t, edge)
                if not o in queue and not o in marked:
                    queue.append(o)
        return traversed

    def get_all_halfedges(self, f):
        return (f[0], f[1]), (f[1], f[2]), (f[2], f[0])

    def edge_info(self):
        edges = []
        for f in self.faces:
            e = self.get_all_halfedges(f)
            edges.append(e[0])
            edges.append(e[1])
            edges.append(e[2])

        # Every edge has a pair edge, since no flag can be paired with multiple
        # edges simply divide by 2
        return edges, len(edges) / 2


# example tests, there will be more
sphere = Variety([(3, 2, 1), (2, 3, 0), (1, 0, 3), (0, 1, 2)])

torus = Variety([
    (1, 0, 3),
    (1, 3, 2),
    (2, 3, 6),
    (3, 4, 6),
    (4, 0, 6),
    (1, 6, 0),
    (2, 6, 5),
    (1, 5, 6),
    (2, 5, 0),
    (3, 0, 5),
    (5, 4, 3),
    (1, 4, 5),
    (1, 2, 4),
    (2, 0, 4),
])



print(sphere.wedge(0,0, lambda x: x, lambda x: -x)(2))
print(sphere.wedge(0,1, lambda x: x, lambda x,y: y-x)(2,3))
print(sphere.wedge(0,2, lambda x: x, lambda x,y,z:  x+y+z if (x-y)*(y-z)*(z-x)>0 else -(x+y+z) )(0,1,2))
print(sphere.wedge(1,1, lambda x,y: x-y, lambda x,y: y-x)(1,2,3))
# print(sphere.check_form(2, lambda x, y, z: x + y + z if (x - y) * (y - z) * (z - x) > 0 else -(x + y + z)))
# print(torus.check_form(1, lambda v, w: 1))
# assert sphere.check() == True
# print('Torus goes')
# print(torus.check())
# print('Shitty surface')
# print(Variety([(1, 2, 3), (2, 3, 0), (3, 0, 1), (0, 1, 2)]).check())
# # print('Not really one surface')
# # assert Variety([(2, 3, 0), (5, 1, 6), (4, 5, 1), (1, 5, 4),(0, 3, 2)]).check() == False
# assert Variety([(1, 2, 0), (1, 0, 2)]).check() == False
# assert Variety(
#     [(3, 2, 1), (2, 3, 0), (1, 0, 3), (0, 1, 2), (6, 5, 4), (5, 6, 0), (4, 0, 6), (0, 4, 5)]).check() == False
