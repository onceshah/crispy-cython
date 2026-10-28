Dijkstra's Algorithm: C vs Python Comparison
============================================

Comparison Parameters:
-----------------------------------------------------------------------
Parameter               C implementation        Python implementation
-----------------------------------------------------------------------
Algorithm               Dijkstra's              Dijkstra's
Graph representation    Adjacency matrix        Adjacency matrix
Edge weights            Non-negative integers   Non-negative integers (Same)
Source vertex           Vertex 0                Vertex 0
Graph size              1000 vertices (Same)    1000 vertices (Same)
Timing method           clock()                 time.perf_counter()
Output                  Execution time          Execution time
-----------------------------------------------------------------------

Requirements:
- Python 3
- C Compiler (MinGW GCC, Clang, or MSVC)

Compilation & Execution on Windows (PowerShell):
1. Compile the C code:
   gcc -O2 dijkstra.c -o dijkstra.exe

2. Run the C implementation:
   .\dijkstra.exe

3. Run the Python implementation:
   python dijkstra.py

Optional Arguments:
Both programs support optional arguments: [vertices] [repeats]
Example:
   .\dijkstra.exe 1000 1
   python dijkstra.py 1000 1

Timing & Metric Details:
- The graph is generated deterministically using the exact same formula in both C and Python.
- Timing strictly measures the Dijkstra shortest-path computation from source vertex 0 (graph generation is excluded).
- Speedup = Python Execution Time / C Execution Time.
