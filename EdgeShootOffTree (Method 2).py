# Calculate a sequence of points, that goes around that tree. Make sure at each branch point in tree we have to sort our children in circular order. So that it goes in a circular order and it self intersections does not happen. (Use Nuance Method)

import matplotlib.pyplot as plt
import random
import math
import json

# Defining a class to store the graph data
class Piecewise_Linear_Graph:
    def __init__(self, vertices, edges):  
        self.vertices = vertices  # Store vertices of the graph
        self.edges = edges  # Store edges of the graph

# Function to check if two lines intersect
def lines_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    
    def ccw(A, B, C):  # Helper function to determine counter-clockwise orientation
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

    # Check if two line segments intersect using orientation tests
    return (ccw((x1, y1), (x3, y3), (x4, y4)) != ccw((x2, y2), (x3, y3), (x4, y4))) and \
           (ccw((x1, y1), (x2, y2), (x3, y3)) != ccw((x1, y1), (x2, y2), (x4, y4)))

# Function to generate a random point on a line segment
def random_point_on_line(x1, y1, x2, y2):
    
    t = random.uniform(0.05, 0.95)  # Randomly select a point between 5% and 95% along the line segment
    
    new_x = ((1 - t) * x1) + (t * x2)  # Calculate x-coordinate of the new point
    new_y = ((1 - t) * y1) + (t * y2)  # Calculate y-coordinate of the new point
    
    return new_x, new_y  # Return the coordinates of the new point

# Function to generate new line segments from a given point
def generate_new_lines(x, y, lines, depth, max_depth, shoot_off_lines):
    
    if depth >= max_depth:  # Base case: stop recursion if maximum depth is reached
        return None  
    
    for j in range(shoot_off_lines):  # Generate specified number of new lines from the current point
        
        attempts = 0  # Counter for attempts to find a non-intersecting line
        
        while attempts < max_attempts:  # Try to generate a non-intersecting line for a limited number of attempts
            
            length = random.uniform(50, 2000)  # Random length for the new line segment
            angle = random.uniform(0, 2 * math.pi)  # Random angle for the direction of the new line
            
            new_x = x + length * math.cos(angle)  # Calculate x-coordinate of the end point of new line
            new_y = y + length * math.sin(angle)  # Calculate y-coordinate of the end point of new line

            intersecting = False  # Flag to check if the new line intersects with existing lines

            for (x1, y1, x2, y2) in lines:  # Check intersection with each existing line segment
                
                if lines_intersect(x, y, new_x, new_y, x1, y1, x2, y2):  # If intersection is found
                    intersecting = True  # Set intersecting flag to True
                    break

            if not intersecting:  # If new line does not intersect with any existing line
                
                color = random.choice(colors)  # Randomly select a color for plotting
                
                axis.plot([x, new_x], [y, new_y], color)  # Plot the new line segment
                lines.append((x, y, new_x, new_y))  # Add the new line segment to the list of lines

                # Recursively generate new lines from a random point on the current line
                random_x, random_y = random_point_on_line(x, y, new_x, new_y)
                generate_new_lines(random_x, random_y, lines, depth + 1, max_depth, shoot_off_lines)
                break

            attempts += 1  # Increment attempt counter

# Function to convert line segments into vertices and edges
def lines_to_list(lines):
    
    vertices = set()  # Set to store unique vertices
    edges = set()  # Set to store unique edges

    for (x1, y1, x2, y2) in lines:  # Iterate over each line segment in the list of lines

        v1 = (round(x1), round(y1))  # Round coordinates to integer values for vertices
        v2 = (round(x2), round(y2))  # Round coordinates to integer values for vertices

        vertices.add(v1)  # Add vertex v1 to the set of vertices
        vertices.add(v2)  # Add vertex v2 to the set of vertices

        edges.add((v1, v2))  # Add edge between v1 and v2 to the set of edges

    vertices = list(vertices)  # Convert set of vertices to a list
    edges = list(edges)  # Convert set of edges to a list

    print("\nThe total number of vertices are: ", len(vertices))  # Print total number of vertices
    print("\nThe total number of edges are: ", len(edges), "\n\n\n\n\n\n\n\n\n\n")  # Print total number of edges

    return vertices, edges  # Return lists of vertices and edges

# Function to write vertices and edges to a JSON file
def write_to_json(graphs, filename):
    
    with open(filename, 'w') as f:  # Open the JSON file for writing

        f.write('{')  # Start writing the JSON object

        for i, graph in enumerate(graphs):  # Iterate over each graph in the list of graphs

            if i > 0:  # Add comma if it's not the first graph
                f.write(',')

            f.write(f'\n\t"Graph{i + 1}": ')  # Write graph index in JSON format
            f.write('\t{\n\t\t\t\t\t"verts": ')  # Write vertices key in JSON format

            json.dump(graph.vertices, f)  # Write vertices list in JSON format

            f.write(',\n\t\t\t\t\t"edges": ')  # Write edges key in JSON format

            json.dump(graph.edges, f)  # Write edges list in JSON format

            f.write('\n\t\t\t\t}\n')  # Close graph object in JSON format

        f.write('\n}')  # Close JSON object

# Main Part
axis = None  # Initialize axis variable for plotting
colors = ['maroon', 'forestgreen', 'blue']  # List of colors for plotting

max_attempts = 3  # Maximum number of attempts to generate a non-intersecting line

iterations = 1 # Number of iterations to generate new lines

max_depth = 5 # Maximum depth of recursion for generating new lines
initial_lines = 5 # Number of initial lines to start from the same point
shoot_off_lines = 3  # Number of lines to shoot off from each random point

generate_graphs = 1  # Number of graphs to generate

graphs = []  # List to store graphs

for k in range(generate_graphs):  # Loop to generate specified number of graphs
    
    lines = []  # List to store line segments
    fig, axis = plt.subplots()  # Create figure and axis for plotting
    
    (initial_x, initial_y) = (640, 360)  # Initial random point
    
    # Generate initial lines from the same point
    for l in range(initial_lines):
        
        length = random.uniform(50, 2000)  # Random length for initial line
        angle = random.uniform(0, 2 * math.pi)  # Random angle for initial line direction

        new_x = initial_x + length * math.cos(angle)  # Calculate x-coordinate of endpoint
        new_y = initial_y + length * math.sin(angle)  # Calculate y-coordinate of endpoint
        
        lines.append((initial_x, initial_y, new_x, new_y))  # Add initial line to list of lines
        axis.plot([initial_x, new_x], [initial_y, new_y], 'black')  # Plot initial line

    # Iteratively shoot off lines from each initial line
    for m in range(iterations):  
        
        for line in list(lines):  # Iterate over a copy of `lines` to avoid infinite loop
        
            x1, y1, x2, y2 = line  # Unpack coordinates of the current line
            
            new_x, new_y = random_point_on_line(x1, y1, x2, y2)  # Generate random point on current line
            
            generate_new_lines(new_x, new_y, lines, 0, max_depth, shoot_off_lines)  # Generate new lines recursively
    
    axis.set_aspect('equal')  # Set equal scaling for x and y axes
    axis.axis('off')  # Turn off axis for cleaner plot
    
    plt.show()  # Display the plot

    vertices, edges = lines_to_list(lines)  # Convert lines to vertices and edges
    
    PL_Graph = Piecewise_Linear_Graph(vertices, edges)  # Create a graph object
    graphs.append(PL_Graph)  # Add graph object to the list of graphs

write_to_json(graphs, 'new_graph_data_shooting_iterative_depth.json')  # Write graphs to JSON file

