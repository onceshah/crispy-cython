# Comprehensive Project & Algorithm Explanation: TSP with C++ & Cython

> **Course / Lab**: SEM 7 — High Performance Python & Cython  
> **Topic**: Graph Algorithms in Production (Part 1: The Traveling Salesperson Problem)  
> **Repository**: [github.com/onceshah/crispy-cython](https://github.com/onceshah/crispy-cython)  
> **PyPI Package**: [pypi.org/project/tsp-fast-solver](https://pypi.org/project/tsp-fast-solver/)  

---

## Table of Contents
1. [Project Overview & Objectives](#1-project-overview--objectives)
2. [The Problem: Traveling Salesperson Problem (TSP)](#2-the-problem-traveling-salesperson-problem-tsp)
3. [Algorithm & Code Walkthrough](#3-algorithm--code-walkthrough)
   - [A. Pure Python Solver (`itertools.permutations`)](#a-pure-python-solver)
   - [B. Native C++ Solver (`std::next_permutation`)](#b-native-c-solver)
   - [C. Cython Wrapper Bridge (`.pxd` and `.pyx`)](#c-cython-wrapper-bridge)
4. [Benchmark Results & Micro-Architectural Analysis](#4-benchmark-results--micro-architectural-analysis)
5. [Build System, Static Linkage & PyPI Packaging](#5-build-system-static-linkage--pypi-packaging)
6. [Complete Project Structure](#6-complete-project-structure)
7. [How to Run, Test, and Verify (Cheatsheet)](#7-how-to-run-test-and-verify-cheatsheet)

---

## 1. Project Overview & Objectives

In production environments, graph algorithms frequently tackle combinatorial optimization problems categorized as **NP-Hard**. When brute-force or exact evaluation is required, dynamic interpreted languages like Python become severe computational bottlenecks due to interpreter overhead and memory indirection.

This project implements a complete, end-to-end production solution:
1. **Pure Python Reference Solver**: Baseline brute-force TSP implementation using standard Python libraries.
2. **Native C++ High-Performance Solver**: Cache-optimized, zero-allocation C++ implementation utilizing modern STL algorithms.
3. **Cython Interfacing Layer**: A high-performance bridge that marshals Python data structures to native C++ vectors and returns the calculated optimal cost.
4. **Performance Benchmark Suite**: Comparative analysis evaluating graph sizes $N=8, 10, 11$, recording a **$112.6\times$ execution speedup**.
5. **Production Distribution**: Configured build pipeline (`setup.py`, `pyproject.toml`, `MANIFEST.in`), packaged into a Source Distribution (`sdist`), and published globally to **PyPI** as `tsp-fast-solver`.
6. **Version Control**: Organized inside a modular GitHub repository `crispy-cython`.

---

## 2. The Problem: Traveling Salesperson Problem (TSP)

### Mathematical Definition
Given a set of $N$ cities labeled $V = \{0, 1, 2, \dots, N-1\}$ and an $N \times N$ distance matrix $D$ where $D_{i,j}$ denotes the travel cost from city $i$ to city $j$:

$$\text{Find a permutation } P = (p_0, p_1, \dots, p_{N-1}) \text{ that minimizes:}$$

$$\text{Cost}(P) = D_{p_0, p_1} + D_{p_1, p_2} + \dots + D_{p_{N-2}, p_{N-1}} + D_{p_{N-1}, p_0}$$

### Combinatorial Complexity
A naive search across all permutations evaluates $N!$ paths. However, because a TSP tour is a closed loop:
- Shifting the starting city produces the same cycle ($0 \to 1 \to 2 \to 0 \equiv 1 \to 2 \to 0 \to 1$).
- Therefore, we can **fix City 0** as the permanent origin and destination.
- We only need to permute the remaining $N - 1$ cities:

$$\text{Search Space} = (N - 1)!$$

#### Growth of $(N - 1)!$:
| Number of Cities ($N$) | Number of Candidate Tours $(N-1)!$ | Feasibility in Pure Python | Feasibility in C++ / Cython |
|:---:|:---:|:---:|:---:|
| $N = 4$ | $3! = 6$ | Instant | Instant |
| $N = 8$ | $7! = 5,040$ | Fast ($< 2\,\text{ms}$) | Sub-millisecond ($0.02\,\text{ms}$) |
| $N = 10$ | $9! = 362,880$ | Noticeable lag ($0.14\,\text{s}$) | Real-time ($1.38\,\text{ms}$) |
| **$N = 11$** | **$10! = 3,628,800$** | **Slow ($1.60\,\text{s}$)** | **Instant ($14.2\,\text{ms}$)** |
| $N = 12$ | $11! = 39,916,800$ | Very slow ($\sim 20 - 30\,\text{s}$) | $\sim 0.15\,\text{s}$ |

---

## 3. Algorithm & Code Walkthrough

### A. Pure Python Solver

File: [`tsp/python_solver/tsp_pure.py`](file:///d:/UPES/SEM%207/Cython/tsp/python_solver/tsp_pure.py)

```python
import itertools
import math

def tsp_python(distance_matrix):
    n = len(distance_matrix)
    if n <= 1:
        return 0
    if n == 2:
        return distance_matrix[0][1] + distance_matrix[1][0]

    # Fix city 0 as start/end, permute cities 1 through n-1
    cities = list(range(1, n))
    min_cost = math.inf

    for perm in itertools.permutations(cities):
        # Leg 1: origin (0) to first city
        cost = distance_matrix[0][perm[0]]

        # Intermediate legs: perm[i] to perm[i+1]
        for i in range(len(perm) - 1):
            cost += distance_matrix[perm[i]][perm[i + 1]]

        # Final leg: return from last city to origin (0)
        cost += distance_matrix[perm[-1]][0]

        if cost < min_cost:
            min_cost = cost

    return min_cost
```

#### Step-by-Step Algorithm:
1. **Base Cases**: $N \le 1$ requires zero travel. $N = 2$ is simply the two-way cost $D_{0,1} + D_{1,0}$.
2. **Permutation Generation**: `itertools.permutations(range(1, n))` yields tuples of size $N-1$.
3. **Cost Accumulation**: Sums edge weights sequentially along the permutation path and finishes with `perm[-1] -> 0`.
4. **Optimal Tracking**: Keeps the running minimum across all $(N-1)!$ tours.

---

### B. Native C++ Solver

Files: [`tsp/cpp/tsp.h`](file:///d:/UPES/SEM%207/Cython/tsp/cpp/tsp.h) and [`tsp/cpp/tsp.cpp`](file:///d:/UPES/SEM%207/Cython/tsp/cpp/tsp.cpp)

#### Header (`tsp.h`):
```cpp
#ifndef TSP_H
#define TSP_H

#include <vector>

int solve_tsp(const std::vector<int>& dist_matrix, int n);

#endif // TSP_H
```

#### Implementation (`tsp.cpp`):
```cpp
#include "tsp.h"
#include <vector>
#include <algorithm>
#include <climits>
#include <numeric>

int solve_tsp(const std::vector<int>& dist_matrix, int n) {
    if (n <= 1) return 0;
    if (n == 2) return dist_matrix[0 * n + 1] + dist_matrix[1 * n + 0];

    // Vector initialized with remaining cities: {1, 2, ..., n-1}
    std::vector<int> cities(n - 1);
    std::iota(cities.begin(), cities.end(), 1);

    int min_cost = INT_MAX;

    // Explore all (n - 1)! permutations in lexicographical order
    do {
        // Leg 1: origin 0 to first city
        int current_cost = dist_matrix[0 * n + cities[0]];

        // Intermediate legs
        for (int i = 0; i < n - 2; ++i) {
            current_cost += dist_matrix[cities[i] * n + cities[i + 1]];
        }

        // Return leg: last city back to 0
        current_cost += dist_matrix[cities[n - 2] * n + 0];

        if (current_cost < min_cost) {
            min_cost = current_cost;
        }
    } while (std::next_permutation(cities.begin(), cities.end()));

    return min_cost;
}
```

#### Why the C++ Implementation is Extremely Fast:
1. **Flattened 1D Memory Model**: The 2D distance matrix of size $N \times N$ is accessed via row-major index arithmetic: `dist_matrix[i * n + j]`. This guarantees contiguous memory access and zero cache misses.
2. **`std::iota`**: Fills the vector with strictly increasing consecutive integers `1, 2, ..., n-1`.
3. **`std::next_permutation`**: Modifies the `cities` array **in-place** to the next lexicographical permutation via quick pointer swaps. It avoids all heap memory allocations during permutation traversal.
4. **Register Variables**: Variables `current_cost`, `min_cost`, and loop counter `i` are stored in CPU hardware registers.

---

### C. Cython Wrapper Bridge

Files: [`tsp/cython_wrapper/tsp_wrapper.pxd`](file:///d:/UPES/SEM%207/Cython/tsp/cython_wrapper/tsp_wrapper.pxd) and [`tsp/cython_wrapper/tsp_wrapper.pyx`](file:///d:/UPES/SEM%207/Cython/tsp/cython_wrapper/tsp_wrapper.pyx)

#### 1. Declaration File (`tsp_wrapper.pxd`):
Tells Cython that an external C++ header `tsp.h` defines `solve_tsp`:
```cython
# distutils: language = c++
from libcpp.vector cimport vector

cdef extern from "tsp.h":
    int solve_tsp(const vector[int]& dist_matrix, int n)
```

#### 2. Implementation File (`tsp_wrapper.pyx`):
```cython
# distutils: language = c++
# cython: language_level = 3

from libcpp.vector cimport vector
from tsp_wrapper cimport solve_tsp

def tsp_cython(object distance_matrix):
    """
    Bridges Python 2D distance matrix to native C++ TSP solver.
    """
    cdef int n = len(distance_matrix)
    if n <= 1:
        return 0
    if n == 2:
        return int(distance_matrix[0][1] + distance_matrix[1][0])

    cdef vector[int] vec
    vec.reserve(n * n)

    cdef int i, j
    for i in range(n):
        row = distance_matrix[i]
        for j in range(n):
            vec.push_back(<int>row[j])

    return solve_tsp(vec, n)
```

#### What Happens Under the Hood:
1. Accepts a standard Python nested list `[[...], [...]]`.
2. Allocates a contiguous C++ `std::vector<int>` with capacity $N^2$ using `vec.reserve(n * n)` to prevent dynamic reallocations.
3. Unpacks Python integers and converts them to 32-bit machine integers (`<int>row[j]`).
4. Hands the vector over to the compiled C++ function `solve_tsp(vec, n)`.
5. The C++ code runs at bare-metal CPU speed, then returns a native `int` which Cython converts back to a Python integer.

---

## 4. Benchmark Results & Micro-Architectural Analysis

File: [`tsp/benchmark.py`](file:///d:/UPES/SEM%207/Cython/tsp/benchmark.py)

### Empirical Results (Recorded on Intel/AMD 64-bit architecture, Python 3.13)

| Graph Size ($N$) | Permutations $(N-1)!$ | Python Time | Cython Time | Speedup Factor |
|:---:|:---:|:---:|:---:|:---:|
| **$N = 8$** | 5,040 | $0.0016\,\text{s}$ | $0.02\,\text{ms}$ | **$67.6\times$** |
| **$N = 10$** | 362,880 | $0.1434\,\text{s}$ | $1.39\,\text{ms}$ | **$103.5\times$** |
| **$N = 11$** | **3,628,800** | **$1.6045\,\text{s}$** | **$14.25\,\text{ms}$** | **$112.6\times$** |

```
Execution Time at N=11:
Pure Python:  ████████████████████████████████████████ 1,604.5 ms
Cython + C++: ▏ 14.2 ms  (>112x Faster)
```

### The 4 Pillars of the 112× Performance Delta

```
┌────────────────────────────────────────────────────────────────────────┐
│                        WHY C++ / CYTHON IS 112× FASTER                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Zero Heap Allocations in Loop:                                      │
│    Python allocates 3.6 million tuple objects during iteration.        │
│    C++ modifies the existing array in-place via std::next_permutation. │
│                                                                        │
│ 2. Cache Locality (L1/L2 Cache Prefetching):                           │
│    Python lists contain pointers to boxed integer objects in RAM.      │
│    C++ std::vector stores numbers contiguously; CPU loads 16 integers  │
│    per 64-byte cache line automatically.                               │
│                                                                        │
│ 3. Direct Machine Code vs Bytecode Interpretation:                     │
│    Python executes 5-10 virtual machine bytecode instructions per sum. │
│    C++ compiles directly to native x86-64 assembly instructions.       │
│                                                                        │
│ 4. Compiler Optimization (-O3):                                        │
│    LLVM/Clang optimizes registers, unrolls loops, and uses branch      │
│    prediction to minimize CPU stalls.                                  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Build System, Static Linkage & PyPI Packaging

### The Standalone Static Linkage Solution
On Windows, compiling C++ extensions with MinGW/LLVM often causes the compiled `.pyd` module to depend on external runtime DLLs (`libc++.dll`, `libunwind.dll`). If end-users do not have these compilers installed, Python raises:
```
ImportError: DLL load failed while importing tsp_wrapper: The specified module could not be found.
```

#### Our Solution in [`tsp/setup.py`](file:///d:/UPES/SEM%207/Cython/tsp/setup.py):
We configured:
```python
extra_compile_args = ["-O3", "-std=c++17"]
extra_link_args = ["-static"]
```
This bakes all C++ standard library dependencies directly into the `.pyd` binary. The resulting extension has **zero external DLL dependencies** beyond standard Windows operating system libraries and `python313.dll`.

### PyPI Source Distribution (`sdist`)
1. **`pyproject.toml`**: Defines build requirements (`setuptools>=61.0`, `cython`), metadata, author, and Python version restrictions (`>=3.8`).
2. **`MANIFEST.in`**: Ensures raw C++ header files (`cpp/tsp.h`), implementations (`cpp/tsp.cpp`), and Cython files (`.pxd`, `.pyx`) are bundled inside the tarball archive.
3. **Building the distribution**:
   ```bash
   python -m build --sdist
   ```
   Generates `dist/tsp_fast_solver-0.1.0.tar.gz`.
4. **Publishing with Twine**:
   ```bash
   python -m twine upload dist/*
   ```
   Authenticated via secure PyPI API Token (`pypi-...`).
5. **Verified Live Installation**:
   ```bash
   pip install tsp-fast-solver
   ```
   Successfully verified that end-user machines download, compile, and execute the library globally.

---

## 6. Complete Project Structure

```
crispy-cython/
│
├── tsp/                                  # Primary assignment module
│   ├── cpp/
│   │   ├── tsp.h                         # Native C++ function prototype
│   │   └── tsp.cpp                       # C++ brute-force implementation
│   ├── cython_wrapper/
│   │   ├── tsp_wrapper.pxd               # External C++ signature declaration
│   │   └── tsp_wrapper.pyx               # Cython bridge function
│   ├── python_solver/
│   │   ├── __init__.py                   # Package export
│   │   └── tsp_pure.py                   # Pure Python reference solver
│   ├── tsp_fast_solver/                  # Pip-installable package namespace
│   │   ├── __init__.py                   # Unified imports: tsp_python & tsp_cython
│   │   └── tsp_pure.py                   # Pure Python solver inclusion
│   ├── tests/
│   │   └── test_tsp.py                   # Pytest suite (edge cases, accuracy)
│   ├── benchmark.py                      # Timing benchmark script (N=8, 10, 11)
│   ├── tsp_wrapper.py                    # Backward compatibility import shim
│   ├── setup.py                          # Cython build and extension compiler
│   ├── pyproject.toml                    # PEP 517 / PEP 621 metadata
│   ├── MANIFEST.in                       # Source distribution file manifest
│   ├── README.md                         # Module-specific documentation
│   └── dist/
│       └── tsp_fast_solver-0.1.0.tar.gz  # PyPI source distribution archive
│
├── dijkstra_c_vs_python/                 # Existing Dijkstra reference comparison
│   ├── dijkstra.c                        # C implementation
│   ├── dijkstra.py                       # Python implementation
│   └── README.txt                        # Dijkstra parameters
│
├── .vscode/
│   ├── settings.json                     # Code-runner config
│   └── tasks.json                        # 1-click VS Code tasks (Benchmark, Test, Build)
│
├── .gitignore                            # Excludes binaries, object files, build artifacts
└── README.md                             # Global repository overview & navigation
```

---

## 7. How to Run, Test, and Verify (Cheatsheet)

### 1. Run the Performance Benchmark
```powershell
cd "d:\UPES\SEM 7\Cython\tsp"
python benchmark.py
```

### 2. Run the Unit Test Suite
```powershell
cd "d:\UPES\SEM 7\Cython\tsp"
python -m pytest tests/
```

### 3. Build the Cython Extension Locally
```powershell
cd "d:\UPES\SEM 7\Cython\tsp"
python setup.py build_ext --inplace
```

### 4. Use the Library in Python
```python
from tsp_fast_solver import tsp_python, tsp_cython

# Example: 4-city distance matrix
dist = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# Both return the exact same optimal cost: 80
print("Pure Python Result:", tsp_python(dist))
print("Cython C++ Result: ", tsp_cython(dist))
```

### 5. Install from PyPI (Globally on any machine)
```powershell
pip install tsp-fast-solver
python -c "import tsp_fast_solver; print('Successfully imported from PyPI!')"
```
