Project 7: Graphs-A\*
=========================

**Due: Thursday, November 30th at 9:00 PM**

_This is not a team project, do not copy someone else’s work._

_This project is more complicated than previous ones, so we suggest starting it early and not leaving it until the last minute. _


## Assignment Overview

### What is A\* Search?

Instead of searching the "next closest" vertex as is done in Dijkstra's algorithm, [A\* Search](https://en.wikipedia.org/wiki/A*_search_algorithm) (A-Star Search) picks the vertex which is "next closest to the goal" by weighting vertices more cleverly.

Recall that in Dijkstra's algorithm, vertices are stored in a priority queue with a priority key equal to the current shortest path to that vertex. If we denote the current shortest path to a vertex *V* by **g(v)**, then on each iteration of Dijkstra's algorithm, we search on the vertex with **min(g(v)).**

A\* search takes the same approach to selecting the next vertex, but instead of setting the priority key of a vertex equal to **g(v)** and selecting **min(g(v))**, it uses the value **f(v)** and selects the vertex with **min(f(v))** where

**f(v) = g(v) + h(v)**

**\= current\_shortest\_path\_to\_v + estimated\_distance\_between\_v\_and\_target**

### In English, Please...

A\* Search prioritizes vertices *V* to search based on the value **f(v)**, which is the sum of

*   **g(v)**, or the current shortest known path to vertex *V*, and
*   **h(v)**, which is the estimated (Euclidean or Taxicab) distance between the vertex *V* and the target vertex you're searching for

The result is that A\* prioritizes vertices to search that (1) are _close to the origin along a known path_ AND which (2) are _in the right direction towards the target._ Vertices with a small **g(v)** are _close to the origin along a known path_ and vertices with a small **h(v)** are _in the right direction towards the target**,**_ so we pick vertices with the smallest sum of these two values.

[We strongly recommend you watch this video to build your intuition behind A\* Search!](https://www.youtube.com/watch?v=ySN5Wnu88nE)

\[A\* is extremely versatile. Here we use Euclidean and Taxicab distances to prioritize certain directions of search, but note that any [metric](https://en.wikipedia.org/wiki/Metric_(mathematics)#Definition) **h(v, target)** could be used should the need arise. See [here](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html) for more information on situations where different metrics may be practical.\]

![AStarGif.gif](https://s3.amazonaws.com/mimirplatform.production/files/002f64b5-cafa-4531-8dc8-e56f0e0de6e6/AStarGif.gif)

Assignment Notes
----------------

*   **We strongly encourage that you read through and thoroughly understand the provided graph methods. You will need to use some of them and understanding the implementation details will save a lot of time.**
*   A plotting function is provided to help you visualize the progression of various search algorithms
    *   Be sure to read the specs explaining **plot()**
    *   If you don't want to use it, just comment out the related import statements and **plot()** function
*   Python allows representation of the value infinity using **float('inf')**
*   No negative edge weights will ever be added to the graph
    *   All edge weights are numeric values greater than or equal to zero
*   Time complexities are specified in terms of *V* and *E*, where *V* represents the number of vertices in the graph and *E* represents the number of edges in a graph
    *   Recall that E is bounded above by *V*^2; a graph has *E* = *V*^2 edges if and only if every vertex is connected to every other vertex
*   Recall that **list.insert(0, element)** and **list.pop(0)** are both _O(N)_ calls on a Python list
    *   Recall that python's 'lists' are not lists in the more common sense of the word: linked lists. They are dynamically managed tuples, stored in memory as contiguous arrays of pointers to elements elsewhere in memory. This allows indexing into a 'list' in constant time. The downside of this, however, is that adding to a python 'list' at a specific index, _i,_ requires shifting the pointer to every element past _i_ by one in the underlying array: a linear operation.
    *   Be careful when implementing **bfs, astar,** and the Application Problem to ensure you do not break time complexity by popping or inserting from the front of a list when reconstructing a path
    *   Instead of inserting into / popping from the front of the list, simply append to or pop from the end, then reverse the list _once_ at the end
        *   If you have N calls to **list.insert(0, element)**, that is _O(N^2)_
        *   If you instead have N calls to **list.append(element)**, followed by a single call to **list.reverse()**, that is _O(N)_
        *   Both methods will result in the same list being constructed, but the second is far more efficient

## Assignment Specifications

### class Vertex

Represents a vertex object, the building block of a graph.

**_DO NOT MODIFY the following attributes/functions_**

*   **Attributes**
    *   **id:** A string used to uniquely identify a vertex
    *   **adj:** A dictionary of type **{other\_id : number}** which represents the connections of a vertex to other vertices; the existence of an entry with key **other\_i****d** indicates connection from this vertex to the vertex with id **other\_id** by an edge with weight **number**
        *   Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures traversals will select the next neighbor to visit deterministically
    *   **visited:** A boolean flag used in search algorithms to indicate that the vertex has been visited
    *   **x:** The x-position of a vertex (used in assignment) (defaults to zero)
    *   **y:** The y-position of a vertex (used in assignment) (defaults to zero)
*   **\_\_init\_\_(self, idx: str, x: float=0, y: float=0) -> None:**  
    *   Constructs a Vertex object
*   **\_\_eq\_\_(self, other: Vertex) -> bool:**
    *   Compares this vertex for equality with another vertex
*   **\_\_repr\_\_(self) -> str:**
    *   Represents the vertex as a string for debugging
*   **\_\_str\_\_(self) -> str:**
    *   Represents the vertex as a string for debugging
*   **\_\_hash\_\_(self) -> int:**
    *   Allows the vertex to be hashed into a set; used in unit tests

**_USE the following function however you'd like_**

*   **deg(self) -> int:**
    *   Returns the number of outgoing edges from this vertex; i.e., the outgoing degree of this vertex
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_outgoing\_edges(self) -> Set\[Tuple\[str, float\]\]:**
    *   Returns a **set** of tuples representing outgoing edges from this vertex
    *   Edges are represented as tuples **(other\_id, weight)** where
        *   **other\_id** is the unique string id of the destination vertex
        *   **weight** is the weight of the edge connecting this vertex to the other vertex
    *   Returns an empty set if this vertex has no outgoing edges
    *   _Time Complexity: O(degV)_
    *   _Space Complexity: O(degV)_
*   **euclidean\_distance(self, other: Vertex) -> float:**
    *   Returns the [euclidean distance](http://rosalind.info/glossary/euclidean-distance/) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
    *   Used in AStar
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **taxicab\_distance(self, other: Vertex) -> float:**
    *   Returns the [taxicab distance](https://en.wikipedia.org/wiki/Taxicab_geometry) \[based on two-dimensional coordinates\] between this vertex and vertex **other**
    *   Used in AStar
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_

### class Graph

Represents a graph object

**_DO NOT MODIFY the following attributes/functions_**

* **Attributes**
    *   **size:** The number of vertices in the graph
    *   **vertices:** A dictionary of type **{id : Vertex}** storing the vertices of the graph, where **id** represents the unique string id of a **Vertex** object
        *   Note that as of Python 3.7, [insertion ordering](https://stackoverflow.com/a/57072435) in normal dictionaries is guaranteed and ensures **get\_edges(self)** and **get\_vertices(self)** will return deterministically ordered lists
    *   **plot\_show**: If true, calls to **plot()** display a rendering of the graph in matplotlib; if false, all calls to **plot()** are ignored (see **plot()** below)
    *   **plot\_delay**: Length of delay in **plot()** (see **plot()** below)
* **\_\_init\_\_(self, plt\_show: bool=False) -> None:**  
    *   Constructs a Graph object
    *   Sets **self.plot\_show** to False by default
* **\_\_eq\_\_(self, other: Graph) -> bool:**
    *   Compares this graph for equality with another graph
* **\_\_repr\_\_(self) -> str:**
    *   Represents the graph as a string for debugging
* **\_\_str\_\_(self) -> str:**
    *   Represents the graph as a string for debugging
* **add\_to\_graph(self, start\_id: str, dest\_id: str=None, weight: float=0) -> float:**
    *   Adds a vertex / vertices / edge to the graph
        *   Adds a vertex with id **start\_id** to the graph if no such vertex exists
        *   Adds a vertex with id **dest\_id** to the graph if no such vertex exists and **dest\_id** is not None
        *   Adds an edge with weight **weight** if **dest\_id** is not None
    *   If a vertex with id **start\_id** or **dest\_id** already exists in the graph, this function will not overwrite that vertex with a new one
    *   If an edge already exists from vertex with id **start\_id** to vertex with id **dest\_id**, this function will overwrite the weight of that edge
* **matrix2graph(self, matrix: Matrix) -> None:**
    *   Constructs a graph from a given adjacency matrix representation
    *   **matrix** is guaranteed to be a square 2D list (i.e. list of lists where # rows = # columns), of size **\[V+1\]** x **\[V+1\]**
        *   **matrix\[0\]\[0\]** is None
        *   The first row and first column of **matrix** hold string ids of vertices to be added to the graph and are symmetric, i.e. **matrix\[i\]\[0\] = matrix\[0\]\[i\]** for i = 1, ..., n
        *   **matrix\[i\]\[j\]** is None if no edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]**
        *   **matrix\[i\]\[j\]** is a **number** if an edge exists from the vertex **matrix\[i\]\[0\]** to the vertex **matrix\[0\]\[j\]** with weight **number**
* **graph2matrix(self) -> None:**
    *   Constructs and returns an adjacency matrix from a graph
    *   The output matches the format of matrices described in **matrix2graph**
    *   If the graph is empty, returns **None**
* **graph2csv(self, filepath: str) -> None:**
    *   Encodes the graph (if non-empty) in a csv file at the given location

* **reset\_vertices(self) -> None:**
    * Resets visited flags to False of all vertices within the graph
    * Used in unit tests to reset graphs between tests
    * Time Complexity: O(V)
    * Space Complexity: O(V)
* **get\_vertex\_by\_id(self, v\_id: str) -> Vertex:**
    * Returns the vertex object with id v_id if it exists in the graph
    * Returns None if no vertex with unique id v_id exists
    * Time Complexity: O(1)
    * Space Complexity: O(1)
* **get\_all\_vertices(self) -> Set\[Vertex\]:**
    * Returns a set of all Vertex objects held in the graph
    * Returns an empty set if no vertices are held in the graph
    * Time Complexity: O(V)
    * Space Complexity: O(V)
* **get\_edge\_by\_ids(self, begin\_id: str, end\_id: str) -> Tuple\[str, str, float\]:**
    * Returns the edge connecting the vertex with id begin_id to the vertex with id end_id in a tuple of the form (begin_id, end_id, weight)
    * If the edge or either of the associated vertices does not exist in the graph, returns None
    * Time Complexity: O(1)
    * Space Complexity: O(1)
* **get\_all\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    * Returns a set of tuples representing all edges within the graph
    * Edges are represented as tuples (begin_id, end_id, weight) where
      * begin_id is the unique string id of the starting vertex
      * end_id is the unique string id of the starting vertex
      * weight is the weight of the edge connecitng the starting vertex to the destination vertex
    * Returns an empty set if the graph is empty
    * Time Complexity: O(V+E)
    * Space Complexity: O(E)
* **build_path(self, back_edges: Dict[str, str], begin_id: str, end_id: str) -> Tuple[List[str], float]:**
    * Given a dictionary of back-edges (a mapping of vertex id to predecessor vertex id), reconstructs the path from start_id to end_id and computes the total distance
    * Returns tuple of the form ([path], distance) where
[path] is a list of vertex id strings beginning with begin_id, terminating with end_id, and including the ids of all intermediate vertices connecting the two
distance is the sum of the weights of the edges along the [path] traveled
    * Handle the cases where no path exists from vertex with id begin_id to vertex with end_id or if one of the vertices does not exist
    * Time Complexity: O(V)
    * Space Complexity: O(V)

**_USE the following function however you'd like_**

*   **plot(self) -> None:**
    *   Renders a visual representation of the graph using matplotlib and displays graphic in PyCharm
        *   [Follow this tutorial to install matplotlib and numpy if you do not have them](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html), or follow the tooltip auto-suggested by PyCharm
    *   Provided for use in debugging
    *   If you call this in your searches and **self.****plot\_show** is true, the search process will be animated in successive plot renderings (with time between frames controlled by **self.plot\_delay**)
    *   Not tested in any testcases
        *   All testcase graphs are constructed with **self.plot\_show** set to False
    *   If vertices have (x,y) coordinates specified, they will be plotted at those locations
    *   If vertices do not have (x,y) coordinates specified, they will be plotted at a random point on the unit circle
    *   To install the necessary packages (matplotlib and numpy), follow the auto-suggestions provided by PyCharm
    *   Vertices and edges are labeled; edges are color-coded by weight
        *   If a bi-directional edge exists between vertices, two color-coded weights will be displayed

![sample_plot.png](https://s3.amazonaws.com/mimirplatform.production/files/0aec2496-150a-4b85-b86f-142f235fe4ba/sample_plot.png)

*   **unvisit\_vertices(self) -> None:**
    *   Resets visited flags of all vertices within the graph
    *   Used in unit tests to reset graph between searches
    *   _Time Complexity: O(V)_
    *   _Space Complexity: O(V)_
*   **get\_vertex(self, vertex\_id: str) -> Vertex:**  
    *   Returns the Vertex object with id **vertex\_id** if it exists in the graph
    *   Returns None if no vertex with unique id **vertex\_id** exists
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_vertices(self) -> Set\[Vertex\]:**  
    *   Returns a **set** of all Vertex objects held in the graph
    *   Returns an empty set if no vertices are held in the graph
    *   _Time Complexity: O(V)_
    *   _Space Complexity: O(V)_
*   **get\_edge(self, start\_id: str, dest\_id: str) -> Tuple\[str, str, float\]:**  
    *   Returns the edge connecting the vertex with id **start\_id** to the vertex with id **dest\_id** in a tuple of the form **(start\_id, dest\_id, weight)**
    *   If the edge or either of the associated vertices does not exist in the graph, returns **None**
    *   _Time Complexity: O(1)_
    *   _Space Complexity: O(1)_
*   **get\_edges(self) -> Set\[Tuple\[str, str, float\]\]:**
    *   Returns a **set** of tuples representing all edges within the graph
    *   Edges are represented as tuples **(start\_id, other\_id, weight)** where
        *   **start\_id** is the unique string id of the starting vertex
        *   **other\_id** is the unique string id of the destination vertex
        *   **weight** is the weight of the edge connecting the starting vertex to the destination vertex
    *   Returns an empty set if the graph is empty
    *   _Time Complexity: O(V+E)_
    *   _Space Complexity: O(E)_

**_IMPLEMENT the following functions_**

* **bfs(self, begin\_id: str, end\_id: str) -> Tuple\[List\[str\], float\]:**
    * Perform a breadth-first search beginning at vertex with id **begin\_id** and terminating at vertex with id **end\_id**
    * **MUST CALL build\_path!**
    * **As you explore from each vertex, iterate over neighbors using vertex.adj (not vertex.get\_edges()) to ensure neighbors are visited in proper order**
    * Returns tuple of the form **(\[path\], distance)** where
        * **\[path\]** is a list of vertex id strings beginning with **begin\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        * **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **begin\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **begin\_id != end\_id** (since that would be a trivial path)
    * Because our adjacency maps use [insertion ordering](https://stackoverflow.com/a/57072435), neighbors will be visited in a deterministic order, and thus you do not need to worry about the order in which you visit neighbor vertices at the same depth
    * Use the [SimpleQueue](https://docs.python.org/3/library/queue.html) class to guarantee O(1) pushes and pops on the queue
    * _Time Complexity: O(V+E)_
    * _Space Complexity: O(V)_
*   **a\_star(self, start\_id: str, target\_id: str, metric: Callable\[\[Vertex, Vertex\], float\]) -> Tuple\[List\[str\], float\]**
    * Perform an A\* search beginning at vertex with id **start\_id** and terminating at vertex with id **end\_id**
    * As you explore from each vertex, iterate over neighbors using **vertex.adj** (not vertex.get\_edges()) to ensure neighbors are visited in proper order
    * Use the **metric** parameter to estimate h(v), the remaining distance, at each vertex
        *   This is a callable parameter and will always be **Vertex.euclidean\_distance** or **Vertex.taxicab\_distance**
    * Returns tuple of the form **(\[path\], distance)** where
        *   **\[path\]** is a list of vertex id strings beginning with **start\_id**, terminating with **end\_id**, and including the ids of all intermediate vertices connecting the two
        *   **distance** is the sum of the weights of the edges along the **\[path\]** traveled
    * If no path exists from vertex with id **start\_id** to vertex with **end\_id** or if one of the vertices does not exist, returns tuple **(\[\],0)**
    * Guaranteed that **start\_id != target\_id** (since that would be a trivial path)
    * Recall that vertices are prioritized in increasing order of **f(v) = g(v) + h(v)**, where
        *   **g(v)** is the shortest known path to this vertex
        *   **h(v)** is the Euclidean distance from *V* to the target vertex
    * Use the given AStarPriorityQueue class to simplify priority key updates in a search priority queue
    * **Implementations of this function which do not utilize the heuristic metric will not receive any credit**
        *   **Do not simply implement Dijkstra's Algorithm**
    * _Time Complexity: O((E + V)log(V))_
    * _Space Complexity: O(V)_

To simplify the operation of updating a priority key in your search priority queue, use the following given class.

### class PriorityQueue

_DO NOT MODIFY the following attributes/functions_

*   **Attributes**
    *   **data:** Underlying data list of priority queue
    *   **locator:** Dictionary to locate vertices within the priority queue
    *   **counter:** Used to break ties between vertices
*   **\_\_init\_\_(self)**  
    *   Constructs an AStarPriorityQueue object
*   **\_\_repr\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **\_\_str\_\_(self)**
    *   Represents the priority queue as a string for debugging
*   **empty(self)**
    *   Returns boolean indicating whether priority queue is empty
*   **push(self, priority, vertex)**  
    *   Push the **vertex** object onto the priority queue with a given **priority** key
    *   This priority queue has been specially designed to hold Vertex objects as values ranked by priority keys; be sure you push Vertex objects and NOT vertex id strings onto the queue
*   **pop(self)**  
    *   Visit, remove and return the Vertex object with the highest priority (i.e. lowest priority key) as a **(priority, vertex)** tuple
*   **update(self, new\_priority, vertex)**
    *   Update the priority of the **vertex** object in the queue to have a **new\_priority**

Application Problem: Star Trek
-------------------

![image.png](https://cdn.europosters.eu/image/750/plastic-frame-star-trek-the-next-generation-enterprise-officers-i83406.jpg)

*“Things are only impossible until they’re not.” –Captain Jean-Luc Picard*

Welcome aboard the [*USS Enterprise*](https://cdn.wallpapersafari.com/86/68/c4fliq.jpg), young Cadet! Your post lies within the navigation team, and today you will be deciding the path we will take to reach our destination, utilizing any wormholes that allow for instantaneous travel between two separate points in space. Since we will be providing you with accurate charts of star systems in the form of a dictionary containing Graphs, we expect you to minimize our dilithium crystal consumption by providing the shortest path from our starting position to our destination. Warp speed does not make sudden changes in course very practical, and we're on a tight schedule, so we'll need your fastest algorithm. A* ought to do it. 

**Complete the following function:**
- **teleport(system_dict, start, end):**
  - system_dict is structured in the following format:
    {system_name: {"graph": Graph object, "arrival_teleport": vertex_name, "departure_teleport": vertex_name,
                           "departure_destinations": [system_names]}}
  - The keys ("graph", "arrival_teleport", "departure_teleport", "departure_destinations") in the inner dictionaries of system_dict are constant and should
    be used in your solution to extract necessary information.
    - "graph": the value associated with this key is the normal Graph class object implemented above
    - "arrival_teleport": the value associated with this key is the name of the vertex in the Graph that will be arrival vertex when teleporting from another system
    - "departure_teleport": the value associated with this key is the name of the vertex in the Graph that will be vertex used to teleporting from this system to another
    - "departure_destinations": the value associated with this key is list of system names connected to departure teleport within this system
    - start: list of strings containing exactly two elements, name of start system, and name of start vertex inside the start system, respectively
    - end: list of strings containing exactly two elements, name of end system, and name of end vertex inside the end system, respectively
  - Returns **distance**
    - **distance** is a float value representing distance from starting vertex to ending vertex
    - If no path exists, return infinity using float('inf')
  - You might need to explore within each system first to find specific distances within systems to help you later
    - Thinking about distance between which two points for each system will be useful
    - The starting system, ending system, and intermediate systems have specific points that will be useful
  - **Several** shortest-path algorithms may be performed to solve this problem. However, there is a solution that only finds one shortest path.
  - Creating a new graph is **allowed** if necessary
  - You are **allowed to use any data structure** you learned in this course for this project if you think it will help you with your solution. But please **note that you must use A\* to solve this application problem. Not using A\* will result in a loss of manual points**.
  - queue.PriorityQueue() **can be used inside this application problem** if necessary
  - V is the number of all vertices, E is the number of all edges, and K is the number of all systems
  - _Time Complexity: O((E + V)log(V))_ 
  - _Space Complexity: O(V + K)_

### Examples
Example 1:

![Example 1](img/APPEX1.png)

This corresponds to the test case:
```python
system_dict = {}
system_a = Graph()
system_a.vertices['A'] = Vertex('A', 0, 0)
system_a.vertices['B'] = Vertex('B', 2, 0)
system_a.vertices['C'] = Vertex('C', 2, 1)
system_a.vertices['D'] = Vertex('D', 2, 2)
system_a.add_to_graph('A', 'B', 2)
system_a.add_to_graph('B', 'C', 2)
system_a.add_to_graph('A', 'D', 7)
system_a.add_to_graph('C', 'D', 1)
system_a_dict = {"graph": system_a, "arrival_teleport": "A", "departure_teleport": "C",
                 "departure_destinations": set()}
# (4.1) There is path within the system
system_dict["System_A"] = system_a_dict
result = teleport(system_dict, ("System_A", "A"), ("System_A", "D"))
expected = 5
self.assertEqual(expected, result)
```
Explanation: 
Green and red indicate the arrival port and departure port of each system. 
This is the normal shortest path problem since there is only a single system. Therefore, the shortest path is A->B->C->D


Example 2:

![Example 2](img/APPEX2_new.png)


This corresponds to the test case:
```python
system_dict = {}
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
             "departure_destinations": {"System_B"}}
system_dict["System_A"] = system_a_dict

system_b = Graph()
system_b.vertices['AJ'] = Vertex('AJ', 5, 5)
system_b.vertices['AB'] = Vertex('AB', 10, 3)
system_b.vertices['AA'] = Vertex('AA', 9, 4)
system_b.vertices['A'] = Vertex('A', 11, 4)
system_b.add_to_graph("AJ", "AB", 10)
system_b.add_to_graph("AB", "AA", 5)
system_b.add_to_graph("AB", "A", 2)
system_b_dict = {"graph": system_b, "arrival_teleport": "AJ", "departure_teleport": "AA",
             "departure_destinations": {"System_A"}}
system_dict["System_B"] = system_b_dict
result = teleport(system_dict, ("System_A", "A"), ("System_B", "A"))
expected = 16
self.assertEqual(expected, result)
```
Explanation: 
Green and red indicate arrival port and departure port of each System.
The start and ending of this example are in different systems, so teleporting between systems is required. 
Therefore, the shortest path is A(System A)->B(System A)->D(System A)->AJ(System B)->AB(System B)->A(System B) which is 16 in distance. **Keep in mind that teleporting does not add any extra distance, so going from D(System A) -> AJ(System B) adds no extra distance to the total.**

Example 3:

![Example 3](img/APPEX3_new.png)

This corresponds to the test case:
```python
system_dict = {}
system_a = Graph()
system_a.vertices['A'] = Vertex('A', 0, 0)
system_a.vertices['B'] = Vertex('B', 1, 0)
system_a.vertices['C'] = Vertex('C', 0, 2)
system_a.vertices['D'] = Vertex('D', 1, 2)
system_a.add_to_graph('A', 'B', 2)
system_a.add_to_graph('A', 'C', 10)
system_a.add_to_graph('B', 'D', 2)
system_a.add_to_graph('C', 'D', 10)
system_a_dict = {"graph": system_a, "arrival_teleport": "C", "departure_teleport": "D",
             "departure_destinations": {"System_B"}}
system_dict["System_A"] = system_a_dict

system_b = Graph()
system_b.vertices['AJ'] = Vertex('AJ', 0, 0)
system_b.vertices['AB'] = Vertex('AB', 0, 1)
system_b.vertices['AA'] = Vertex('AA', 1, 1)
system_b.vertices['A'] = Vertex('A', 1, 0)
system_b.add_to_graph("AJ", "AB", 3)
system_b.add_to_graph("AB", "AA", 2)
system_b.add_to_graph("AB", "A", 2)
system_b_dict = {"graph": system_b, "arrival_teleport": "AJ", "departure_teleport": "AA",
             "departure_destinations": {"System_A"}}
system_dict["System_B"] = system_b_dict
result = teleport(system_dict, ("System_A", "A"), ("System_A", "C"))
expected = 9
self.assertEqual(expected, result)
```
Explanation: 
Green and red indicate arrival port and departure port of each system.
Even if the starting and ending star are in the same system, your solution must be able to find a shortest path that teleports between galaxies.
In this case, the shortest path from System A: A to System A: C is A(System A) -> B(System A) -> D(System A) -> AJ(System B) -> AB(System B) -> AA(System B) -> C(System A)
which is 9 in distance.

Example 4:

![Example 4](img/APPEX4.png)

This corresponds to the test case:
```python
system_dict = {}
system_a = Graph()
system_a.vertices['A'] = Vertex('A', 0, 0)
system_a.vertices['B'] = Vertex('B', 0, 1)
system_a.vertices['C'] = Vertex('C', 1, 1)
system_a.vertices['D'] = Vertex('D', 2, 2)
system_a.vertices['E'] = Vertex('E', 0, 2)
system_a.add_to_graph('A', 'B', 1)
system_a.add_to_graph('A', 'C', 2)
system_a.add_to_graph('B', 'E', 1)
system_a.add_to_graph('C', 'D', 3)
system_a.add_to_graph('E', 'D', 2)
system_a_dict = {"graph": system_a, "arrival_teleport": "A", "departure_teleport": "D",
             "departure_destinations": {"System_B", "System_C"}}
system_dict["System_A"] = system_a_dict

system_b = Graph()
system_b.vertices['A'] = Vertex('A', 0, 0)
system_b.vertices['C'] = Vertex('C', 1, 1)
system_b.vertices['D'] = Vertex('D', 2, 3)
system_b.add_to_graph("A", "C", 10)
system_b.add_to_graph("C", "D", 3)
system_b_dict = {"graph": system_b, "arrival_teleport": "A", "departure_teleport": "D",
             "departure_destinations": {"System_D"}}
system_dict["System_B"] = system_b_dict

system_c = Graph()
system_c.vertices['A'] = Vertex('A', 1, 2)
system_c.vertices['B'] = Vertex('B', 2, 1)
system_c.vertices['D'] = Vertex('D', 4, 2)
system_c.vertices['E'] = Vertex('E', 3, 1)
system_c.add_to_graph("A", "D", 5)
system_c.add_to_graph("E", "D", 2)
system_c.add_to_graph("B", "E", 1)
system_c.add_to_graph("A", "B", 2)
system_c_dict = {"graph": system_c, "arrival_teleport": "A", "departure_teleport": "D",
             "departure_destinations": {"System_D"}}
system_dict["System_C"] = system_c_dict

system_d = Graph()
system_d.vertices['A'] = Vertex('A', 5, 5)
system_d.vertices['B'] = Vertex('B', 6, 5)
system_d.vertices['C'] = Vertex('C', 4, 4)
system_d.vertices['D'] = Vertex('D', 6, 6)
system_d.add_to_graph("A", "D", 2)
system_d.add_to_graph("D", "B", 1)
system_d.add_to_graph("B", "A", 4)
system_d.add_to_graph("C", "D", 6)
system_d = {"graph": system_d, "arrival_teleport": "A", "departure_teleport": "D",
             "departure_destinations": {}}
system_dict["System_D"] = system_d_dict


result = teleport(system_dict, ("System_A", "A"), ("System_D", "B"))
expected = 12
self.assertEqual(expected, result)
```
Explanation: 
Green and red indicate arrival port and departure port of each system.
The expected shortest path start from System A at point A. Then, the shortest path from A(System A) -> Departure point of System A is 4 costs, A -> B -> E -> D. 
Then, the spaceship will travel across systems to reach destination system(D).
The shortest path from departure point of System A to destination system has cost of 4 which is pass through system C, distance from arrival port to departure port in C is 5, A -> D.
Eventually, spaceship reaches destination system and finds the shortest path from arrival port to destination star within that system which is A -> D -> B (3 costs).
The total of distance is 4 + 5 + 3 = 12


### Hints
Many students have issues with how to go from one system to another. Below, we provide some hints regarding this:

* For a given system, the departure_teleport is the vertex that a teleport can be done, and the departure_destinations are the systems it can teleport to. Teleporting costs nothing, and when a teleport is done to the destination system, the ship will arrive at the arrival teleport vertex. It can kind of be thought of in that sense as 0-weight edges connecting the teleport departures and arrivals.

* You can go to any of the systems in departure_destinations if you first find a path to departure_teleport. If you can’t find the end vertex in your current system, you need to calculate the distance from the start to the departure_teleport vertex and then find the node in the neighbor systems.
For example, let’s say we have two systems- A and B. These are connected via teleportation. If you want to calculate the distance between a start vertex in A to an end vertex in B, all you have to do is calculate the distance between the start vertex and the departure point of A and add that to the distance between the arrival point of B and the end vertex.

* Be careful about the space complexity when connecting systems. One possible solution is to create a new, larger graph with a new name and use the add_to_graph() or matrix2graph() functions instead of combining the systems.

* Beware of the edge-cases, there are a lot of things to consider, try thinking about them before writing your code, and thinking about how you can solve them. Ex: You start at System A, and finish at System A, but because this is a directed graph, there might not be a direct path from the starting node in System A to the destination node in the same system, but there might be a way by going through other system...

# **Submission Guidelines**

### **Deliverables:**

For each project, a `solution.py` file will be provided. Ensure to write your Python code within this file. For best results:
- 📥 **Download** both `solution.py` and `tests.py` to your local machine.
- 🛠️ Use **PyCharm** for a smoother coding and debugging experience.

### **How to Work on a Project Locally:**

Choose one of the two methods below:

---

#### **APPROACH 1: Using D2L for Starter Package**
1. 🖥️ Ensure PyCharm is installed.
2. 📦 **Download** the starter package from the *Projects* tab on D2L. *(See the tutorial video on D2L if needed)*.
3. 📝 Write your code and, once ready, 📤 **upload** your `solution.py` to Codio. *(Refer to the D2L tutorial video for help)*.

---

#### **APPROACH 2: Directly from Codio**
1. 📁 On your PC, create a local folder like `Project01`.
2. 📥 **Download** `solution.py` from Codio.
3. 📥 **Download** `tests.py` from Codio for testing purposes.
4. 🛠️ Use PyCharm for coding.
5. 📤 **Upload** the `solution.py` back to Codio after ensuring the existing file is renamed or deleted.
6. 🔚 Scroll to the end in Codio's Guide editor and click the **Submit** button.

---

### **Important:**
- Always **upload** your solution and **click** the 'Submit' button as directed.
- All project submissions are due on Codio. **Any submission after its deadline is subject to late penalties** .
  
**Tip:** While Codio can be used, we recommend working locally for a superior debugging experience in PyCharm. Aim to finalize your project locally before submitting on Codio.


### Deliverables:

Please submit your solution.py  by November 30th 9:00 pm. Click Submit and Mark Complete. 
    

### Grading

The following 100-point rubric will be used to determine your grade on Project 7

* Policies
  * Using a different algorithm than the one specified for some function will result in the loss of all automated and manual points for that function.

* tests (70)
   * 1 - **bfs** : \_\_/12
   * 2 - **a\_star** : \_\_/28
   * 3 - **teleport** : \_\_/30 

* Manual (30)

  * Time and space complexity points are **all-or-nothing** for each function. If you fail to meet time or space complexity in a given function, you do not receive manual points for that function.
    * Loss of 1 point per missing docstring (max 5 point loss)
    * Loss of 2 points per changed function signature (max 20 point loss)
    * We reserve the right to deduct points for any other issues we find in your code.
    * Manual points for each function require passing all tests for that function.
  
  * Time & Space Complexity (28)
    * M1 - **bfs** :\_\_/6
      * _Time Complexity: O(V+E)_ 
      * _Space Complexity: O(V)_
    * M2 - **a\_star**: \_\_/10
      * _Trust that our heuristic function is admissible, consistent and calculated in O(1) time._
      * _The log(V) comes from using a priority queue._
      * _Time Complexity: O((V + E)log(V))_ 
      * _Space Complexity: O(V)_
    * M3 - **teleport**:\_\_/12
      * E and V are total counts of edges and vertices across all graphs, respectively.
      * _Time Complexity: O((V + E)log(V))_ 
      * _Space Complexity: O(V + K)_
      
* Feedback (2)


### Congratulations on Finishing your Last Project! 
* [What time is it?!](https://youtu.be/3hOP7qPDyI4)

