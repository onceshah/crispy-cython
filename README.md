# crispy-cython ⚡

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![C++17](https://img.shields.io/badge/C++-17-00599C.svg?logo=c%2B%2B)](https://en.cppreference.com/w/cpp/17)
[![Cython](https://img.shields.io/badge/Cython-3.0+-gold.svg)](https://cython.org/)
[![PyPI](https://img.shields.io/pypi/v/tsp-fast-solver.svg)](https://pypi.org/project/tsp-fast-solver/)

A collection of high-performance graph, combinatorial, and mathematical algorithms implemented in native **C/C++**, accelerated and interfaced to Python via **Cython**, and benchmarked against pure Python reference implementations.

---

## 📂 Repository Structure

| Module / Algorithm | Description | Tech Stack | Published Package |
|---|---|---|---|
| **[`tsp/`](./tsp/)** | Brute-force Traveling Salesperson Problem solver achieving **$112\times$ speedup** over pure Python. | C++ (`std::next_permutation`), Cython, Python | [`tsp-fast-solver`](https://pypi.org/project/tsp-fast-solver/) on PyPI |
| **[`dijkstra_c_vs_python/`](./dijkstra_c_vs_python/)** | Single-source shortest path Dijkstra's algorithm benchmark on dense graphs. | C (`gcc -O2`), Python | Local executable & script |
| *More to come...* | Additional graph algorithms, dynamic programming, and numerical solvers. | C/C++, Cython, OpenMP | *Future modules* |

---

## 🚀 Quick Navigation

- **Traveling Salesperson Problem (TSP)**: Detailed documentation, C++ code, Cython wrapper, and benchmark suite are in the **[`tsp/`](./tsp/)** folder.
  - Install via pip: `pip install tsp-fast-solver`
  - Run benchmark: `cd tsp && python benchmark.py`
- **Dijkstra's Algorithm**: See **[`dijkstra_c_vs_python/`](./dijkstra_c_vs_python/)** for C vs Python execution time analysis.

---

## 📄 License
This repository is licensed under the [MIT License](LICENSE).
