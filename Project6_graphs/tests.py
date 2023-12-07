import unittest, string, math, random, cProfile
from xml.dom import minidom
from numpy import matrix

from solution import Graph, Vertex, teleport


class GraphTests(unittest.TestCase):

    def test_bfs(self):
        graph = Graph()

        # (1) test on empty graph
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (2) test on graph missing begin or dest
        graph.add_to_graph('a')
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))
        subject = graph.bfs('b', 'a')
        self.assertEqual(subject, ([], 0))

        # (3) test on graph with both vertices but no path
        graph.add_to_graph('b')
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, ([], 0))

        # (4) test on single edge
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        subject = graph.bfs('a', 'b')
        self.assertEqual(subject, (['a', 'b'], 331))

        # (5) test on two edges
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        subject = graph.bfs('a', 'c')
        self.assertEqual(subject, (['a', 'b', 'c'], 431))

        # (6) test on edge triangle and ensure one-edge path is taken
        # (bfs guarantees fewest-edge path, not least-weighted path)
        graph = Graph()
        graph.add_to_graph('a', 'b', 331)
        graph.add_to_graph('b', 'c', 100)
        graph.add_to_graph('a', 'c', 999)
        subject = graph.bfs('a', 'c')
        self.assertEqual(subject, (['a', 'c'], 999))

        # (7) test on grid figure-8 and ensure fewest-edge path is taken
        graph = Graph(csvf='test_csvs/bfs/7.csv')

        subject = graph.bfs('bottomleft', 'topleft')
        self.assertEqual(subject, (['bottomleft', 'midleft', 'topleft'], 2))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('bottomright', 'topright')
        self.assertEqual(subject, (['bottomright', 'midright', 'topright'], 2))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('bottomleft', 'topright')
        self.assertIn(subject[0], [['bottomleft', 'midleft', 'topleft', 'topright'],
                                   ['bottomleft', 'midleft', 'midright', 'topright'],
                                   ['bottomleft', 'bottomright', 'midright', 'topright']])
        self.assertEqual(subject[1], 3)

        # (8) test on example graph from Onsay's slides, starting from vertex A
        # see bfs_graph.png
        graph = Graph(csvf='test_csvs/bfs/8.csv')

        subject = graph.bfs('a', 'd')
        self.assertEqual(subject, (['a', 'b', 'd'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'f')
        self.assertEqual(subject, (['a', 'c', 'f'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'h')
        self.assertEqual(subject, (['a', 'e', 'h'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'g')
        self.assertEqual(subject, (['a', 'e', 'g'], 4))

        graph.unvisit_vertices()  # mark all unvisited
        subject = graph.bfs('a', 'i')
        self.assertIn(subject[0], [['a', 'e', 'h', 'i'], ['a', 'e', 'g', 'i']])
        self.assertEqual(subject[1], 6)

        # (9) test path which does not exist
        graph.unvisit_vertices()  # mark all unvisited
        graph.add_to_graph('z')
        subject = graph.bfs('a', 'z')
        self.assertEqual(subject, ([], 0))

    def test_a_star(self):

        # PART ONE -- SMALLER TEST CASES

        # === Edge Cases === #

        # (1) test on empty graph
        graph = Graph()
        subject = graph.a_star('a', 'b', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))

        # (2) start/end vertex does not exist
        graph = Graph()
        graph.add_to_graph('a')
        # (2.1) start vertex
        subject = graph.a_star('b', 'a', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))
        # (2.2) end vertex
        subject = graph.a_star('a', 'b', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))

        # (3) test for path which does not exist
        graph = Graph()
        graph.add_to_graph('a', 'b')
        subject = graph.a_star('b', 'a', lambda v1, v2: 0)
        self.assertEqual(subject, ([], 0))

        # === (A) Grid graph tests ===#
        graph = Graph()

        # (1) test on nxn grid from corner to corner: should shoot diagonal
        # (shortest path is unique, so each heuristic will return the same path)
        grid_size = 5
        for x in range(grid_size):
            for y in range(grid_size):
                idx = f"{x},{y}"
                graph.vertices[idx] = Vertex(idx, x, y)
        for x in range(grid_size):
            for y in range(grid_size):
                if x < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                    graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                if y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                    graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                if x < grid_size - 1 and y < grid_size - 1:
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            subject = graph.a_star('0,0', '4,4', metric)
            self.assertEqual(subject[0], ['0,0', '1,1', '2,2', '3,3', '4,4'])
            self.assertAlmostEqual(subject[1], (grid_size - 1) * math.sqrt(2))
            graph.unvisit_vertices()

        # (2) test on nxn grid with penalty for shooting diagonal
        # (shortest path is not unique, so each heuristic will return a different path)
        for x in range(grid_size - 1):
            for y in range(grid_size - 1):
                graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        subject = graph.a_star('0,0', '4,4', Vertex.euclidean_distance)
        self.assertEqual(subject, (['0,0', '1,0', '1,1', '2,1', '2,2', '3,2', '3,3', '4,3', '4,4'], 8))
        graph.unvisit_vertices()
        subject = graph.a_star('0,0', '4,4', Vertex.taxicab_distance)
        self.assertEqual(subject, (['0,0', '1,0', '2,0', '3,0', '4,0', '4,1', '4,2', '4,3', '4,4'], 8))
        graph.unvisit_vertices()

        # === (B) Tollway graph tests ===#
        graph = Graph(csvf='test_csvs/astar/tollway_graph_csv.csv')
        # now must set of coordinates for each vertex:
        positions = [(0, 0), (2, 0), (4, 0), (7, 0), (10, 0), (12, 0), (2, 5), (6, 4), (12, 5), (5, 9), (8, 8), (12, 8),
                     (8, 10), (0, 2),
                     (4, 2), (9, 2), (9, -2), (7, 6), (8, 11), (14, 8)]

        for index, v_id in enumerate(list(graph.vertices)):
            graph.vertices[v_id].x, graph.vertices[v_id].y = positions[index]

        # UMCOMMENT TO SEE PLOT
        # graph.plot_show = True
        # graph.plot()

        for metric in [Vertex.euclidean_distance, Vertex.taxicab_distance]:
            # (3) test Franklin Grove to Northbrook shortest path in both directions
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Franklin Grove', 'Northbrook', metric)
            solution = (['Franklin Grove', 'A', 'B', 'G', 'J', 'M', 'Northbrook'], 22)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Northbrook', 'Franklin Grove', metric)
            solution = (['Northbrook', 'M', 'J', 'G', 'B', 'A', 'Franklin Grove'], 22)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            # (4) test Franklin Grove to Joliet shortest path - bypass expensive tollway path
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Franklin Grove', 'Joliet', metric)
            solution = (['Franklin Grove', 'A', 'B', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Joliet', 'Franklin Grove', metric)
            solution = (['Joliet', 'E', 'D', 'H', 'G', 'B', 'A', 'Franklin Grove'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            # (5) test Joliet to Chicago shortest path - bypass expensive tollway path
            # (shortest path is unique, so each heuristic will return the same path)
            subject = graph.a_star('Joliet', 'Chicago', metric)
            solution = (['Joliet', 'E', 'D', 'H', 'G', 'J', 'K', 'L', 'Chicago'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Chicago', 'Joliet', metric)
            solution = (['Chicago', 'L', 'K', 'J', 'G', 'H', 'D', 'E', 'Joliet'], 35)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            # (6) test Northbrook to Belvidere - despite equal path lengths, A* heuristic will always prefer search to the left
            # (both heuristics will prefer the same path)
            subject = graph.a_star('Northbrook', 'Belvidere', metric)
            solution = (['Northbrook', 'M', 'J', 'K', 'Belvidere'], 8)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

            subject = graph.a_star('Belvidere', 'Northbrook', metric)
            solution = (['Belvidere', 'K', 'J', 'M', 'Northbrook'], 8)
            self.assertEqual(subject, solution)
            graph.unvisit_vertices()

        # PART 2 -- BIGGER TEST CASES

        # === (C) Random graph tests ===#
        # (1) initialize vertices of Euclidean and Taxicab weighted random graphs
        random.seed(331)
        probability = 0.5  # probability that two vertices are connected
        e_graph, t_graph = Graph(), Graph()
        vertices = []
        for s in string.ascii_lowercase:
            x, y = random.randint(0, 100), random.randint(0, 100)
            vertex = Vertex(s, x, y)
            vertices.append(vertex)
            e_graph.vertices[s], t_graph.vertices[s] = vertex, vertex
            e_graph.size += 1
            t_graph.size += 1

        # (2) construct adjacency matrix with edges weighted by appropriate distance metric
        e_matrix = [[None] + [s for s in string.ascii_lowercase]]
        t_matrix = [[None] + [s for s in string.ascii_lowercase]]
        for i in range(1, len(e_matrix[0])):
            e_row = [e_matrix[0][i]]
            t_row = [t_matrix[0][i]]
            for j in range(1, len(e_matrix[0])):
                connect = (random.random() < probability)  # connect if random draw in (0,1) < probability
                e_weighted_dist, t_weighted_dist = None, None
                if i != j and connect:
                    e_dist = vertices[i - 1].euclidean_distance(vertices[j - 1])
                    t_dist = vertices[i - 1].taxicab_distance(vertices[j - 1])
                    weight = (random.randint(1, 10))  # choose a random weight between 1 and 9
                    e_weighted_dist = e_dist * weight  # create realistic weighted dist
                    t_weighted_dist = t_dist * weight  # create realistic weighted dist
                e_row.append(e_weighted_dist)
                t_row.append(t_weighted_dist)
            e_matrix.append(e_row)
            t_matrix.append(t_row)
        e_graph.matrix2graph(e_matrix)
        t_graph.matrix2graph(t_matrix)

        # (3) define helper function to check validity of search result
        def is_valid_path(graph, search_result):
            path, dist = search_result
            length = 0
            for i in range(len(path) - 1):
                begin, end = path[i], path[i + 1]
                edge = graph.get_edge_by_ids(begin, end)
                if edge is None:
                    return False  # path contains some edge not in the graph
                length += edge[2]
            return length == dist  # path consists of valid edges: return whether length matches

        # (4) test all 26 x 26 pairwise A* traversals across random matrix and ensure they return valid paths w/o error
        for begin in vertices:
            for end in vertices:
                if begin != end:
                    subject = e_graph.a_star(begin.id, end.id, Vertex.euclidean_distance)
                    self.assertTrue(is_valid_path(e_graph, subject))
                    e_graph.unvisit_vertices()

                    subject = t_graph.a_star(begin.id, end.id, Vertex.taxicab_distance)
                    self.assertTrue(is_valid_path(t_graph, subject))
                    t_graph.unvisit_vertices()

    def test_teleport(self):

        # PART ONE -- SMALL TEST CASES
        # -- EDGE CASES --
        # (1) Empty galaxy
        galaxy_dict = {}
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_A", "B"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (2) Missing star in galaxy
        galaxy_dict = {}
        system_a = Graph()
        system_a.vertices['A'] = Vertex('A', 0, 0)
        system_a.vertices['B'] = Vertex('B', 1, 1)
        system_a.add_to_graph('A', 'B', 2)
        system_a_dict = {"graph": system_a, "arrival_teleport": "A", "departure_teleport": "B",
                         "departure_destinations": {"System_B"}}
        galaxy_dict["System_A"] = system_a_dict

        # (2.1) Missing end vertex
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_A", "C"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (2.2) Missing end vertex
        result = teleport(galaxy_dict, ("System_A", "C"), ("System_A", "A"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (2.3) Missing both vertices
        result = teleport(galaxy_dict, ("System_A", "D"), ("System_A", "C"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (3) Missing galaxies
        galaxy_dict = {}
        system_a = Graph()
        system_a.vertices['A'] = Vertex('A', 0, 0)
        system_a.vertices['B'] = Vertex('B', 1, 1)
        system_a.add_to_graph('A', 'B', 2)
        system_a_dict = {"graph": system_a, "arrival_teleport": "A", "departure_teleport": "D",
                         "departure_destinations": {"System_B"}}

        system_b = Graph()
        system_b.vertices['AA'] = Vertex('AA', 0, 0)
        system_b.vertices['BB'] = Vertex('BB', 5, 1)
        system_b.add_to_graph('A', 'B', 10)
        system_b_dict = {"graph": system_b, "arrival_teleport": "A", "departure_teleport": "BB",
                         "departure_destinations": {"System_A"}}
        galaxy_dict["System_A"] = system_a_dict
        galaxy_dict["System_B"] = system_b_dict
        # (3.1) Missing ending system

        result = teleport(galaxy_dict, ("System_A", "A"), ("System_D", "C"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (3.2) Missing end system
        result = teleport(galaxy_dict, ("System_D", "C"), ("System_A", "A"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (3.3) Missing both systems
        result = teleport(galaxy_dict, ("System_D", "D"), ("System_AG", "C"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (4) Testing one system
        galaxy_dict = {}
        system_a = Graph()
        system_a.vertices['A'] = Vertex('A', 0, 0)
        system_a.vertices['B'] = Vertex('B', 2, 0)
        system_a.vertices['C'] = Vertex('C', 2, 1)
        system_a.vertices['D'] = Vertex('D', 2, 2)
        system_a.add_to_graph('A', 'B', 3)
        system_a.add_to_graph('B', 'C', 2)
        system_a.add_to_graph('A', 'D', 7)
        system_a.add_to_graph('C', 'D', 1)
        system_a_dict = {"graph": system_a, "arrival_teleport": "A", "departure_teleport": "C",
                         "departure_destinations": set()}
        # (4.1) There is path within system
        galaxy_dict["System_A"] = system_a_dict
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_A", "D"))
        expected = 6
        self.assertEqual(expected, result)

        # (4.2) There is no path within system
        galaxy_dict["System_A"] = system_a_dict
        result = teleport(galaxy_dict, ("System_A", "D"), ("System_A", "A"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (5) Test on multiple systems 1
        galaxy_dict = {}
        system_a = Graph()
        system_a.vertices['A'] = Vertex('A', 0, 0)
        system_a.vertices['B'] = Vertex('B', 1, 0)
        system_a.vertices['C'] = Vertex('C', 0, 2)
        system_a.vertices['D'] = Vertex('D', 1, 2)
        system_a.add_to_graph('A', 'B', 2)
        system_a.add_to_graph('A', 'C', 6)
        system_a.add_to_graph('B', 'D', 2)
        system_a.add_to_graph('C', 'D', 1)
        system_a_dict = {"graph": system_a, "arrival_teleport": "A", "departure_teleport": "D",
                         "departure_destinations": {"System_B", "System_C"}}
        galaxy_dict["System_A"] = system_a_dict

        system_b = Graph()
        system_b.vertices['AJ'] = Vertex('AJ', 5, 5)
        system_b.vertices['AB'] = Vertex('AB', 10, 3)
        system_b.vertices['AA'] = Vertex('AA', 9, 4)
        system_b.vertices['A'] = Vertex('A', 11, 4)
        system_b.add_to_graph("AJ", "AB", 10)
        system_b.add_to_graph("AB", "AA", 5)
        system_b.add_to_graph("AB", "A", 2)
        system_b_dict = {"graph": system_b, "arrival_teleport": "AJ", "departure_teleport": "AA",
                         "departure_destinations": {"System_C"}}
        galaxy_dict["System_B"] = system_b_dict

        system_c = Graph()
        system_c.vertices['A'] = Vertex('A', 0, 0)
        system_c.vertices['D'] = Vertex('D', 4, 0)
        system_c.vertices['J'] = Vertex('J', 0, 3)
        system_c.vertices['E'] = Vertex('E', 5, 0)
        system_c.add_to_graph("A", "D", 5)
        system_c.add_to_graph("A", "J", 4)
        system_c.add_to_graph("J", "E", 10)
        system_c.add_to_graph("E", "J", 8)
        system_c.add_to_graph("D", "E", 1)

        system_c_dict = {"graph": system_c, "arrival_teleport": "A", "departure_teleport": "J",
                         "departure_destinations": {"System_B"}}
        galaxy_dict["System_C"] = system_c_dict

        # (5.1) Test within the same system
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_A", "B"))
        expected = 2
        self.assertEqual(expected, result)
        # (5.2) Test no path within system
        result = teleport(galaxy_dict, ("System_A", "C"), ("System_A", "A"))
        expected = float('inf')
        self.assertEqual(expected, result)

        # (5.3) Test across system
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_B", "A"))
        expected = 16
        self.assertEqual(expected, result)
        # (5.4) Test across system continue
        result = teleport(galaxy_dict, ("System_A", "D"), ("System_B", "AJ"))
        expected = 0
        self.assertEqual(expected, result)

        # (5.5) Test across system continue
        result = teleport(galaxy_dict, ("System_A", "C"), ("System_C", "E"))
        expected = 7
        self.assertEqual(expected, result)

        # (5.5) Test starting at departure point
        result = teleport(galaxy_dict, ("System_C", "J"), ("System_B", "AB"))
        expected = 10
        self.assertEqual(expected, result)

        # (5.6) Test Teleport points act as cycle
        result = teleport(galaxy_dict, ("System_C", "E"), ("System_C", "D"))
        expected = 28
        self.assertEqual(expected, result)

        # (6) Test multiple system 2
        galaxy_dict = {}
        system_a = Graph()
        system_a.vertices['A'] = Vertex('A', 0, 0)
        system_a.vertices['B'] = Vertex('B', 1, 0)
        system_a.vertices['C'] = Vertex('C', 0, 2)
        system_a.vertices['D'] = Vertex('D', 1, 2)
        system_a.add_to_graph('A', 'B', 10)
        system_a.add_to_graph('A', 'C', 20)
        system_a.add_to_graph('B', 'D', 20)
        system_a.add_to_graph('C', 'D', 1)
        system_a_dict = {"graph": system_a, "arrival_teleport": "C", "departure_teleport": "B",
                         "departure_destinations": {"System_B"}}
        galaxy_dict["System_A"] = system_a_dict

        system_b = Graph()
        system_b.vertices['A'] = Vertex('A', 0, 0)
        system_b.vertices['B'] = Vertex('B', 0, 1)
        system_b.vertices['C'] = Vertex('C', 1, 2)
        system_b.vertices['D'] = Vertex('D', 2, 3)
        system_b.add_to_graph('A', 'B', 1)
        system_b.add_to_graph('B', 'C', 2)
        system_b.add_to_graph('A', 'D', 5)
        system_b.add_to_graph('D', 'C', 2)
        system_b_dict = {"graph": system_b, "arrival_teleport": "A", "departure_teleport": "C",
                         "departure_destinations": {"System_A"}}
        galaxy_dict["System_B"] = system_b_dict

        # (6.1) Testing wrap instead of direct travel
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_A", "D"))
        expected = 14
        self.assertEqual(expected, result)

        # (6.2) Testing normal traversal
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_A", "B"))
        expected = 10
        self.assertEqual(expected, result)

        # (6.2) Testing normal traversal
        result = teleport(galaxy_dict, ("System_A", "A"), ("System_B", "B"))
        expected = 11
        self.assertEqual(expected, result)

        # PART TWO -- Larger test case

        def create_grid_graph(graph, grid_size):
            for x in range(grid_size):
                for y in range(grid_size):
                    idx = f"{x},{y}"
                    graph.vertices[idx] = Vertex(idx, x, y)
            for x in range(grid_size):
                for y in range(grid_size):
                    if x < grid_size - 1:
                        graph.add_to_graph(f"{x},{y}", f"{x + 1},{y}", 1)
                        graph.add_to_graph(f"{x + 1},{y}", f"{x},{y}", 1)
                    if y < grid_size - 1:
                        graph.add_to_graph(f"{x},{y}", f"{x},{y + 1}", 1)
                        graph.add_to_graph(f"{x},{y + 1}", f"{x},{y}", 1)
                    if x < grid_size - 1 and y < grid_size - 1:
                        graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", math.sqrt(2))
                        graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", math.sqrt(2))

            # (2) test on nxn grid with penalty for shooting diagonal
            # (shortest path is not unique, so each heuristic will return a different path)
            for x in range(grid_size - 1):
                for y in range(grid_size - 1):
                    graph.add_to_graph(f"{x},{y}", f"{x + 1},{y + 1}", 3)
                    graph.add_to_graph(f"{x + 1},{y + 1}", f"{x},{y}", 3)

        # (1.) Large three grid graph
        galaxy_dict = {}
        graph_a = Graph()
        create_grid_graph(graph_a, grid_size=5)
        system_a_dict = {"graph": graph_a, "arrival_teleport": "0,1", "departure_teleport": "3,4",
                         "departure_destinations": {"System_B", "System_C"}}
        galaxy_dict["System_A"] = system_a_dict

        graph_b = Graph()
        create_grid_graph(graph_b, grid_size=3)
        system_b_dict = {"graph": graph_b, "arrival_teleport": "0,0", "departure_teleport": "1,0",
                         "departure_destinations": {"System_C"}}
        galaxy_dict["System_B"] = system_b_dict

        graph_c = Graph()
        create_grid_graph(graph_c, grid_size=6)
        system_c_dict = {"graph": graph_c, "arrival_teleport": "5,3", "departure_teleport": "5,5",
                         "departure_destinations": set()}
        galaxy_dict["System_C"] = system_c_dict

        # (1.1) Testing normal traversal within same system
        result = teleport(galaxy_dict, ("System_A", "0,0"), ("System_A", "4,4"))
        expected = 8
        self.assertAlmostEqual(expected, result)

        # (1.2) Testing normal traversal within same system
        result = teleport(galaxy_dict, ("System_B", "2,0"), ("System_B", "1,1"))
        expected = 2
        self.assertAlmostEqual(expected, result)

        # (1.3) Testing normal traversal within same system
        result = teleport(galaxy_dict, ("System_C", "0,0"), ("System_C", "5,5"))
        expected = 10
        self.assertAlmostEqual(expected, result)

        # (1.4) Testing across systems
        result = teleport(galaxy_dict, ("System_A", "0,0"), ("System_B", "1,1"))
        expected = 9
        self.assertAlmostEqual(expected, result)

        # (1.5) Testing across systems
        result = teleport(galaxy_dict, ("System_A", "0,0"), ("System_C", "5,5"))
        expected = 9
        self.assertAlmostEqual(expected, result)

        # (1.6) Testing across systems
        result = teleport(galaxy_dict, ("System_B", "0,0"), ("System_C", "5,5"))
        expected = 3
        self.assertAlmostEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
