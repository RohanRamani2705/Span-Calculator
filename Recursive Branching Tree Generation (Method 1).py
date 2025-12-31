# Calculate a sequence of points, that goes around that tree. Make sure at each branch point in tree we have to sort our children in circular order. So that it goes in a circular order and it self intersections does not happen. (Use Nuance Method)


import matplotlib.pyplot as plt
import random
import math
import json

class Picewise_Linear_Graph:
    
    def __init__(self, vertices, edges):
        
        self.vertices = vertices
        self.edges = edges

# Function to check if two lines intersect
def lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    return ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4)) and \
           ccw((x1, y1), (x2, y2), (x3, y3)) != ccw((x1, y1), (x2, y2), (x4, y4))

# Function to generate node
def generate_node(x, y, branches, depth, lines):
    
    if depth >= max_depth: # If depth is greater than max_depth then exit
        return
    
    for i in range(branches): # Using a for loop to iterate over the branches created and create new branches
    
        attempts = 0 # Initial value
        
        while attempts < max_attempts: # Using a while loop until a non intersecting point has been found (Limited attempts)
            
            length = random.uniform(100, 200) # Random length
            angle = random.uniform(0, 2 * math.pi) # Random angle between 0 and 2π
            
            new_x = x + length * math.cos(angle) # Using the trignometic formula x = r * cos(θ) to calculate the new x coordinate at the endpoint of the branch 
            new_y = y + length * math.sin(angle) # Using the trignometic formula y = r * sin(θ) to calculate the new y coordinate at the endpoint of the branch 
            
            intersecting = False # Initialzing a flag to keep track
            
            for (x1, y1, x2, y2) in lines: # Looping through all lines
            
                if lines_intersect(x, y, new_x, new_y, x1, y1, x2, y2): # If lines intersect with any other lines
                    
                    intersecting = True
                    
                    break # It will go back to the start and try again
                    
        
            if not intersecting: # If the lines are not intersecting
                
                color = random.choice(colors) # Giving random colours
                    
                axis.plot([x, new_x], [y, new_y], color) # Plotting the points
                
                lines.append((x, y, new_x, new_y)) # Adding the new line to the list
                
                generate_node(new_x, new_y, branches, depth + 1, lines) # Calling this function again in a loop to generate the children branches recursively
                
                break
            
            attempts += 1 # Each times it goes to the start, it will add +1 and stop at a certain value and plot the graph

# Creating a function to convert the set of lines into 2 different list
def lines_to_list(lines):
    
    vertices = set() # Using a set for vertices so that it can remove the duplicates
    edges = set() # Using a set for vertices so that it can remove the duplicates

    for (x1, y1, x2, y2) in lines: # Looping through all lines
        
        v1 = (round(x1), round(y1))
        v2 = (round(x2), round(y2))
        
        vertices.add((v1, v1)) # Adding v1 to vertices
        vertices.add((v2, v2)) # Adding v2 to vertices
        
        edges.add((v1, v2)) # Add v1,v2 as edges to edges
    
    vertices = list(vertices) # Using a list to store vertices
    edges = list(edges) # Usinga list to store edges
    
    print("\nThe total no of vertices are: ", len(vertices)) # Finding the length of vertices
    print("\nThe total no of edges are: ", len(edges), "\n\n") # Finding the length of the edges
    
    return vertices, edges

# Function to write vertices and edges to a JSON file
def write_to_json(graphs, filename):
    
    # Opening the specified file at write mode
    with open(filename, 'w') as f:
    
        # Writing the JSON content
        f.write('{')
        
        for i, graph in enumerate(graphs): # Looping through each graph in a list of graphs
            
            # Add comma before each graph except the first one
            if i > 0:
                f.write(',')
            
            # Formatting
            f.write(f'\n\t"Graph{i + 1}": ')
            
            f.write('\t{\n\t\t\t\t\t"verts": ')
            
            json.dump(graph.vertices, f)
            
            # Formatting
            f.write(',\n\t\t\t\t\t"edges": ')
            
            json.dump(graph.edges, f)
            
            # Formatting
            f.write('\n\t\t\t\t}\n')
        
        f.write('\n}')

# Main Part
axis = None
colors = ['maroon', 'forestgreen', 'blue'] 

max_attempts = 3 # Giving max_attempts, so that it doesnt get stuck
    
max_depth = 3
initial_branches = 3

generate_graphs = 1

graphs = [] # Creating a List to store generated graphs

for i in range(generate_graphs):
    
    lines = [] # Creating a list to keep track of all the lines
    
    fig, axis = plt.subplots() # Creating a new figure and axis for plotting
    
    generate_node(640, 360, initial_branches, 0, lines) # Generating tree
    
    axis.set_aspect('equal')
    axis.axis('off')
    
    plt.show() # Displaying the Tree
    
    # Calling the function to convert the set of lines into a list of vertices and a list of edges
    vertices, edges = lines_to_list(lines) 
    
    # Creating an instance of the Picewise_Linear_Graph class with vertices and edges as arguments
    PL_Graph = Picewise_Linear_Graph(vertices, edges)
    
    graphs.append(PL_Graph) # Appending the newly created graph object to the list of graphs

# Calling the function to write the vertices and edges to a text file
write_to_json(graphs, 'graph_data_recursive.json')

# Calculate a sequence of points, that goes around that tree. Make sure at each branch point in tree we have to sort our children in circular order. So that it goes in a circular order and it self intersections does not happen. (Use Nuance Method)


# Limit the decimals to 2 places upon line geenration
# Generate Random keys using ASCII Codes for verts

