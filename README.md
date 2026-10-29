# crispy-cython ⚡

[![PyPI version](https://img.shields.io/pypi/v/tsp-fast-solver.svg?color=blue)](https://pypi.org/project/tsp-fast-solver/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/tsp-fast-solver.svg)](https://pypi.org/project/tsp-fast-solver/)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-00599C.svg?logo=c%2B%2B)](https://en.cppreference.com/w/cpp/17)
[![Cython 3.0+](https://img.shields.io/badge/Cython-3.0+-gold.svg)](https://cython.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A curated collection of high-performance graph, combinatorial, and mathematical algorithms implemented in native **C/C++**, accelerated and interfaced to Python via **Cython**, and benchmarked against pure Python reference implementations.

Published on PyPI: `pip install tsp-fast-solver`

---

## 📊 Benchmark Spotlight: Traveling Salesperson Problem (TSP)

![TSP Performance Benchmark](tsp_benchmark_comparison.png)

```
======================================================================================
        TRAVELING SALESPERSON PROBLEM (TSP) PRODUCTION BENCHMARK        
             Pure Python (itertools) vs C++ (Cython Wrapper)            
======================================================================================
 CPU / System : 13th Gen Intel Core i7-13700HX (16C/24T) | Windows 11 (64-bit)
 Memory (RAM) : 16 GB DDR5
 Python Env   : Python 3.13.7 (64-bit) | Compiler: Clang/LLVM-MinGW (-O3 -std=c++17 -static)
 Timing Clock : timeit.default_timer (High-precision monotonic QPC hardware clock)
 Sampling     : Multi-run sample averaging (10 runs for N=8,10; 3-5 runs for N=11)
======================================================================================
Graph Size (N)   | Possible Routes (N-1)!   | Python Time   | Cython Time   | Speedup   
----------------------------------------------------------------------------------------
N = 8            | 5,040                    | 1.65 ms       | 0.021 ms      | ~79x      
N = 10           | 362,880                  | 145.2 ms      | 1.39 ms       | ~104x     
N = 11           | 3,628,800                | 1.61 s        | 14.3 ms       | ~112.6x   
----------------------------------------------------------------------------------------
```

> **Key Finding**: At $N = 11$, our C++ Cython solver evaluates **3,628,800 candidate closed tours in just 14 milliseconds**, delivering a **$112.6\times$ speedup** over standard Python. Notice how the acceleration ratio scales up as $N$ grows — this is because Python's per-iteration interpreter overhead compounds factorially.

---

## 🔬 Why is C++ with Cython 112× Faster?

```
┌────────────────────────────────────────────────────────────────────────┐
│                        ARCHITECTURAL BOTTLENECK ANALYSIS               │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Zero Heap Allocations in Loop:                                      │
│    Python allocates 3.6 million tuple objects during iteration.        │
│    C++ modifies the existing array in-place via std::next_permutation. │
│                                                                        │
│ 2. Cache Locality (L1/L2 Cache Prefetching):                           │
│    Python lists store references to separated PyObject integers in RAM.│
│    C++ std::vector stores numbers contiguously; CPU loads 16 integers  │
│    per 64-byte cache line automatically.                               │
│                                                                        │
│ 3. Direct Machine Code vs Bytecode Interpretation:                     │
│    Python executes 5-10 virtual machine bytecode opcodes per leg.      │
│    C++ compiles directly to native x86-64 assembly instructions.       │
│                                                                        │
│ 4. Compiler Optimization (-O3):                                        │
│    LLVM/Clang optimizes registers, unrolls loops, and uses branch      │
│    prediction to minimize CPU pipeline stalls.                         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Quickstart

### 1. Installation via PyPI
You can install and use the compiled TSP solver directly from PyPI without configuring C++ compilers:

```bash
pip install tsp-fast-solver
```

### 2. Python Usage Example
```python
from tsp_fast_solver import tsp_python, tsp_cython

# Define a 4-city distance matrix
distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# Compute optimal closed-tour cost
py_cost = tsp_python(distance_matrix)
cy_cost = tsp_cython(distance_matrix)

print(f"Optimal TSP Tour Cost (Python): {py_cost}")  # Output: 80
print(f"Optimal TSP Tour Cost (Cython): {cy_cost}")  # Output: 80
```

---

## 🧩 Algorithm Walkthrough

### Pure Python Reference (`tsp/python_solver/tsp_pure.py`)
Fixes City 0 as origin and generates $(N-1)!$ permutations of remaining cities using `itertools.permutations`:
```python
import itertools, math

def tsp_python(distance_matrix):
    n = len(distance_matrix)
    if n <= 1: return 0
    if n == 2: return distance_matrix[0][1] + distance_matrix[1][0]

    cities = list(range(1, n))
    min_cost = math.inf

    for perm in itertools.permutations(cities):
        cost = distance_matrix[0][perm[0]]
        for i in range(len(perm) - 1):
            cost += distance_matrix[perm[i]][perm[i + 1]]
        cost += distance_matrix[perm[-1]][0]

        if cost < min_cost:
            min_cost = cost
    return min_cost
```

### Native C++ Optimized Core (`tsp/cpp/tsp.cpp`)
Uses row-major contiguous memory indexing (`dist_matrix[i * n + j]`), `std::iota`, and in-place `std::next_permutation`:
```cpp
#include "tsp.h"
#include <vector>
#include <algorithm>
#include <climits>
#include <numeric>

int solve_tsp(const std::vector<int>& dist_matrix, int n) {
    if (n <= 1) return 0;
    if (n == 2) return dist_matrix[0 * n + 1] + dist_matrix[1 * n + 0];

    std::vector<int> cities(n - 1);
    std::iota(cities.begin(), cities.end(), 1); // [1, 2, ..., n-1]

    int min_cost = INT_MAX;

    do {
        int current_cost = dist_matrix[0 * n + cities[0]];
        for (int i = 0; i < n - 2; ++i) {
            current_cost += dist_matrix[cities[i] * n + cities[i + 1]];
        }
        current_cost += dist_matrix[cities[n - 2] * n + 0];

        if (current_cost < min_cost) {
            min_cost = current_cost;
        }
    } while (std::next_permutation(cities.begin(), cities.end()));

    return min_cost;
}
```

### Cython Bridge (`tsp/cython_wrapper/tsp_wrapper.pyx`)
Marshals Python nested lists into a pre-reserved 1D `std::vector<int>` and delegates computation directly to compiled machine code:
```cython
from libcpp.vector cimport vector
from tsp_wrapper cimport solve_tsp

def tsp_cython(object distance_matrix):
    cdef int n = len(distance_matrix)
    if n <= 1: return 0
    if n == 2: return int(distance_matrix[0][1] + distance_matrix[1][0])

    cdef vector[int] vec
    vec.reserve(n * n)

    cdef int i, j
    for i in range(n):
        row = distance_matrix[i]
        for j in range(n):
            vec.push_back(<int>row[j])

    return solve_tsp(vec, n)
```

---

## ⚖️ Engineering Guidelines: When to Use Cython

| Scenario | Recommend Cython? | Rationale |
|---|:---:|---|
| **CPU-Bound Loops** | ✅ **YES** | Inner loops, combinatorial state exploration, numerical matrix math. |
| **Graph Traversals** | ✅ **YES** | Eliminates pointer chasing and object instantiation overhead. |
| **DSP & Physics Simulation** | ✅ **YES** | Enables SIMD vectorization and register-level arithmetic. |
| **I/O-Bound Tasks** | ❌ **NO** | Waiting on network, disk, or database latency makes CPU gains negligible. |
| **High-Level Glue Code** | ❌ **NO** | Premature optimization increases build complexity and maintenance cost. |
| **Rapid Prototyping** | ❌ **NO** | Python’s dynamic agility is better suited for early iteration. |

---

## 📂 Repository Layout

```
crispy-cython/
├── tsp/                                  # Traveling Salesperson Problem Module
│   ├── cpp/                              # Native C++ core
│   │   ├── tsp.h                         # C++ header definition
│   │   └── tsp.cpp                       # In-place std::next_permutation solver
│   ├── cython_wrapper/                   # Cython interface layer
│   │   ├── tsp_wrapper.pxd               # External C++ signature declarations
│   │   └── tsp_wrapper.pyx               # Vector conversion & Python bridge
│   ├── python_solver/                    # Pure Python baseline
│   │   ├── __init__.py                   # Package export
│   │   └── tsp_pure.py                   # itertools.permutations solver
│   ├── tsp_fast_solver/                  # PyPI package source
│   ├── tests/                            # Unit test suite (pytest)
│   ├── benchmark.py                      # Multi-sample benchmark runner
│   ├── setup.py                          # Setuptools with -O3 -static build
│   ├── pyproject.toml                    # PEP 517 build metadata
│   ├── MANIFEST.in                       # Source distribution manifest
│   └── README.md                         # Detailed TSP technical report
├── dijkstra_c_vs_python/                 # Dijkstra Shortest Path Module
│   ├── dijkstra.c                        # Native C implementation
│   ├── dijkstra.py                       # Python reference implementation
│   └── README.txt                        # Execution instructions
├── tsp_benchmark_comparison.png          # High-resolution benchmark chart
├── EXPLANATION.md                        # Complete project architectural report
├── LINKEDIN_POST.md                      # Community technical post draft
├── LICENSE                               # MIT License
└── README.md                             # Global project documentation
```

---

## 🛠️ Developer Guide (Running Locally)

### Run Benchmark
```bash
cd tsp
python benchmark.py
```

### Run Unit Tests
```bash
cd tsp
python -m pytest tests/
```

### Recompile Cython In-Place
```bash
cd tsp
python setup.py build_ext --inplace
```

### Generate High-Res Infographic Chart
```bash
python generate_chart.py
```

---

## 🗺️ Roadmap
- [x] Traveling Salesperson Problem (Pure Python vs C++ Cython)
- [x] Standalone static Windows `.pyd` compilation (`-static`)
- [x] PyPI release (`tsp-fast-solver`)
- [ ] Multithreaded TSP search using OpenMP (`#pragma omp parallel for`)
- [ ] Branch-and-Bound / Dynamic Programming (Held-Karp) comparisons
- [ ] Additional Graph Solvers: Floyd-Warshall & Bellman-Ford

---

## 📄 License
This project is open source and distributed under the [MIT License](LICENSE).  
Copyright (c) 2026 Vansh Shah.
