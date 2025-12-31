Span Calculator

Introduction:

Welcome to the Span Calculator! This project is a powerful tool designed to compute and visualize spanning structures over a given graph. Whether you're a student, researcher, or graph theory enthusiast, this tool simplifies complex graph operations with a clear visual representation.

What is a Span?
In graph theory, a span represents a subset of edges that connects all vertices without creating cycles, typically forming a tree-like structure. The Span Calculator uses algorithms to calculate this structure and helps visualize it interactively.

Key Features:

Graph Visualization: Displays the graph and its spanning structure.
Kruskal's Algorithm: Efficiently finds the Minimum Spanning Tree (MST).
Component Mapping: Computes surjective spans between graph components.
Interactive Interface: Visualize results dynamically using Pygame.

How it Works:

1️) Graph Representation

The graph is loaded from a JSON file.
Each vertex is represented by its coordinates.
Edges connect pairs of vertices with a weight based on their distance.

2️) Distance and Weight Calculation

The distance between two points is calculated using the Euclidean formula.
Edge weights are determined based on these distances.

3️) Spanning Tree Calculation (Kruskal's Algorithm)

Edges are sorted by weight.
Edges are added to the spanning tree without forming cycles.
The algorithm continues until all vertices are connected.

4️) Surjective Span Computation

Components of the graph are identified.
A surjective mapping ensures every vertex is part of the final span.
Duplicate connections are avoided for clarity.

5️) Visualization with Pygame

The graph and its spanning tree are rendered on a Pygame window.
Vertices and edges are color-coded for clarity.
Interactive controls allow you to explore the graph.


Installation and Setup:

Clone the repository: 
git clone https://github.com/yourusername/span-calculator.git

Navigate to the project directory:
cd span-calculator

Install dependencies:
pip install -r requirements.txt

Run the program:
python main.py

Usage Instructions:
Place your graph data in graph.json.
Run the program and observe the visualization.
Use keyboard/mouse controls to interact with the graph.

Example Graph Input (graph.json)

{
  "vertices": [
    [0, 0], [1, 2], [3, 4]
  ],
  "edges": [
    [0, 1], [1, 2]
  ]
}


Troubleshooting

If the graph doesn't render, ensure the JSON file is formatted correctly.
Install any missing dependencies using pip install.


Thank you for checking out the Span Calculator. Happy graph exploring!

✨ If you find this project useful, consider giving it a star on GitHub! 🌟
