import pygame
import json
import random
import numpy

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

#Graph struct.
class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges    = edges
        self.points   = self.makePTsDict()
        
    def makePTsDict(self):
        ptDict = {}
        for v in self.vertices:
            ptDict.update({v[0]: v[1]})
        return ptDict

#Component struct.
class Component:
    def __init__(self, set_of_vertices, set_of_edges, set_horizontal_projection, set_vertical_projection):
        self.vertices              = set_of_vertices            # initially a single vertex...
        self.edges                 = set_of_edges
        self.vertical_projection   = set_vertical_projection    # edge[0][1], edge[1][1]
        self.horizontal_projection = set_horizontal_projection  # edge[0][0], edge[1][0]
    
    def add_edge(self, v1, v2): # Where v1 and v2 are pairs of vertices from the base graph.
        self.edges.add((v1, v2))
        if v1[0] == v2[0]:
            self.vertical_projection.add((v1[1], v2[1]))
        else:
            self.horizontal_projection.add((v1[0], v2[0]))
        
    def print_component(self):
        print(f"Component vertices              = {self.vertices}")
        print(f"Component edges                 = {self.edges}")
        print(f"Component horizontal_projection = {self.horizontal_projection}")
        print(f"....horizontal_projection len = {len(self.horizontal_projection)}")
        print(f"Component vertical_projection   = {self.vertical_projection}")
        print(f"....vertical_projection len = {len(self.vertical_projection)}")
        print( "---------------------------------")
        
        
def component_union(comp1, comp2):
    unioned_vertices              = comp1.vertices | comp2.vertices
    unioned_edges                 = comp1.edges | comp2.edges
    unioned_horizontal_projection = comp1.horizontal_projection | comp2.horizontal_projection
    unioned_vertical_projection   = comp1.vertical_projection | comp2.vertical_projection
    return Component(unioned_vertices, unioned_edges, unioned_horizontal_projection, unioned_vertical_projection)

#Draw function. Only in 2D.
def drawPLGraph(aGraph):
    for vert in aGraph.vertices:
        pygame.draw.circle(screen, "green", (vert[1][0], vert[1][1]), 4)
    for edge in aGraph.edges:
        pygame.draw.line(screen, "green", (aGraph.points[edge[0]][0], aGraph.points[edge[0]][1]), (aGraph.points[edge[1]][0], aGraph.points[edge[1]][1]))

#Generates a spanning forrest using Kruskal's algorithm.
def kruskalAlgorithm(aGraph, vert_len = 0, return_components = False):
    kruskal_components = []
    x, y = 0, 0
    
    #Initialize list of kruskal_components with vertices paired with edges. [({},{}), ...]
    for v in aGraph.vertices:
        vertSet = {v[0]}
        edgeSet = set()
        for e in aGraph.edges:
            if v in e:
                edgeSet.add(e)
        kruskal_components.append((vertSet,edgeSet))
    
    #Combines sets together to find kruskal_components.
    for edge in aGraph.edges:
        for i in range(len(kruskal_components)):
            if edge[0] in kruskal_components[i][0]:
                x = i
            if edge[1] in kruskal_components[i][0]:
                y = i
        if x == y:
            continue
        else:
            kruskal_components[x][0].update(kruskal_components[y][0])
            kruskal_components[x][1].update(kruskal_components[y][1])
            kruskal_components.remove(kruskal_components[y])
        #print(kruskal_components, '\n\n')  #prints updated kruskal_components[] one step at a time,
    #print(kruskal_components)              #will print just the final state.
    
    for c in kruskal_components:
        print(f"component vertices: \n{c[0]}\ncomponent edges: \n{c[1]}")
    
    if(len(kruskal_components)>1):
        print("There are ", len(kruskal_components), " components")
    else: 
        print("There is 1 component.")
        
    if return_components:
        return kruskal_components

#Convert JSON arrays into desired tuple form.
def listToTuple(aList):
    newList = []
    for item in aList:
        newList.append((tuple(item[0]), tuple(item[1])))

    return(newList)

#Loads piecewise linear graph information from JSON file.
def loadGraph(filename):
    f        = open(filename, "r")
    file     = json.load(f)
    vertList = listToTuple(file["Graph6"]["verts"]) # [[[v_name],[v_position]], [[v_name],[v_position]], [[v_name],[v_position]], ....]
    edgeList = listToTuple(file["Graph6"]["edges"]) # [[v1,v2], [v3,v4], [v5,v6], ....]  Each pair of vertices makes up an edge.
    f.close()
    return vertList, edgeList

#Testing variables/objects for code execution.
filename = "GraphData\graph_data.json"
fileVerts, fileEdges = loadGraph(filename)
fileGraph = Graph(fileVerts, fileEdges)
#kruskalAlgorithm(fileGraph)


def check_distance(p1, p2):
    return numpy.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)
    
def check_distance_higher_dim(p1, p2):
    distance_vector = vector_from_points(p1,p2)
    return numpy.sqrt(calc_dot_product(distance_vector, distance_vector))

def vector_from_points(p1, p2):
    vector_result = []

    for element in range(len(p1)):
        e1 = p1[element]
        e2 = p2[element]
        
        vector_result.append(e2 - e1)
        
    return vector_result

def calc_dot_product(u, v):
    dot_product = 0.
    element_products = []
        
    # Take the product of corresponding elements.
    for element in range(len(u)):
        element_products.append((u[element] * v[element]))
    
    # Add everything together.
    for i in range(len(element_products)):
        dot_product += element_products[i]
    
    return dot_product

def calc_weight(q, p1, p2):
    u = vector_from_points(p1, p2)
    v = vector_from_points(p1, q)
    
    u_dot_v = calc_dot_product(u, v)
    u_dot_u = calc_dot_product(u, u)
    
    scalar = u_dot_v / u_dot_u
    scalar = min(1., max(0., scalar)) # clamp scalar to range [0,1]                                                # By Dr. Logan Hoehn
    p = [p1[i] + scalar*u[i] for i in range(len(p1))]   ### Consider using tuples instead of lists for all vectors #
    return check_distance_higher_dim(p,q)                                                                          #

# May not be tottaly correct. Only checks for ENTIRE edge. Could underestimate the surjective span.
# Could still be a good approximation with many small straight segments. Subdivide as needed.
def Compute_Surjective_Span(aGraph):
    print(f"Begin t-val check.")
    
    points = aGraph.points
    product_verts = []
    product_edges = []
    weights       = dict()
    
    for v1 in points.keys():    # setting up product_verts
        for v2 in points.keys():
            product_verts.append((v1,v2))
    
    for vert in points.keys():  # setting up product_edges and calculating weights.
        for edge in aGraph.edges:
            product_edges.append(((edge[0], vert), (edge[1], vert)))
            product_edges.append(((vert, edge[0]), (vert, edge[1])))
            
            w = calc_weight(points[vert], points[edge[0]], points[edge[1]])
            
            weights[((edge[0], vert), (edge[1], vert))] = round(w, 2)
            weights[((vert, edge[0]), (vert, edge[1]))] = round(w, 2)
            
        #    print(f"Weight of {(vert, vert)} with edge {edge} = {w}")
        #print("--------------------------------------------------------------------------------------------------------------------------------------------------")
    
    product_graph = Graph(product_verts, product_edges)
    
    #print(f"Graph verts:\n{product_graph.vertices}\n")
    #print(f"Graph edges:\n{product_graph.edges}\n")
    #
    #print(f"Sorted weights:")
    #for edge in sorted(product_graph.edges, key = lambda e: weights[e], reverse = True):
    #    print(f"edge = {edge}       weight = {weights[edge]}")
    
    components = set()
    
    # Initialize set of component objects. One for each vertex in TxT.
    for vertex in product_verts:
        init_component = Component({vertex}, set(), set(), set())
        components.add(init_component)
    
    # Add edges to components one at a time from highest weight to lowest until the horizontal and vertical projection of a component are onto.
    # Return the weight of the most recently added edge once onto is found.
    for edge in sorted(product_graph.edges, key = lambda e: weights[e], reverse = True):
        for comp in components:                                                          # By Dr. Logan Hoehn
            #print(f"checking edge {edge} with component {comp}")
            if edge[0] in comp.vertices:
                comp1 = comp
            if edge[1] in comp.vertices:
                comp2 = comp
        if comp1 == comp2:
            comp = comp1
        else:
            comp = component_union(comp1, comp2)
            components.add(comp)
            #print(f"Combining {comp1.vertices} with {comp2.vertices}")
            #comp.print_component()
            components.remove(comp1)
            components.remove(comp2)
            
        comp.add_edge(edge[0], edge[1])
        
        # Checks for onto condition.
        if len(comp.horizontal_projection) == len(aGraph.edges) and len(comp.vertical_projection) == len(aGraph.edges):
            print(f"WEIGHT IS {weights[edge]}")
            print(f"t-val check end. Weight found.")
            return weights[edge]
    
    print(f"t-val check end. No onto component found.")

bleh = Compute_Surjective_Span(fileGraph)

# Basic game loop from pygame documentation.
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((50,50,50,255))

    # RENDER YOUR GAME HERE
    
    drawPLGraph(fileGraph)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
