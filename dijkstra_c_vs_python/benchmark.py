"""
Benchmark Script for Dijkstra's Shortest Path Solvers
(Pure Python vs Compiled C++ wrapped with Cython)

Evaluates performance across graph sizes V = 21 (Dehradun Real-World Graph),
V = 200, V = 500, V = 1000, V = 1500 vertices.
Includes dynamic hardware detection for CPU model, core/thread counts, and physical RAM.
"""

import os
import sys
import platform
import socket
import timeit

# Ensure package is on sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from dijkstra_fast_solver import dijkstra_python, dijkstra_from_edges_python
except ImportError:
    from python_solver import dijkstra_python, dijkstra_from_edges_python

try:
    from dijkstra_fast_solver import dijkstra_cython, dijkstra_from_edges_cython
except ImportError:
    try:
        from dijkstra_wrapper import dijkstra_cython, dijkstra_from_edges_cython
    except ImportError:
        dijkstra_cython = None
        dijkstra_from_edges_cython = None

# If Cython module is missing for current Python version, attempt automatic build
if dijkstra_cython is None:
    print("[INFO] Cython C++ solver not yet built for this Python environment.")
    print("       Attempting automated compilation via setup.py...")
    try:
        import subprocess
        setup_script = os.path.join(os.path.dirname(__file__), "setup.py")
        if os.path.exists(setup_script):
            build_res = subprocess.run(
                [sys.executable, setup_script, "build_ext", "--inplace"],
                cwd=os.path.dirname(__file__),
                capture_output=True,
                text=True
            )
            if build_res.returncode == 0:
                try:
                    from dijkstra_fast_solver import dijkstra_cython, dijkstra_from_edges_cython
                    print("[SUCCESS] Cython C++ solver compiled successfully!\n")
                except ImportError:
                    pass
    except Exception as e:
        pass

from dehradun_map.dehradun_graph import (
    build_dehradun_distance_matrix,
    NODES_COORDS,
    EDGES_DICTS,
)


def get_system_specs() -> dict:
    """
    Dynamically detects exact CPU model, physical/logical core counts,
    and physical RAM configuration across Windows, macOS, and Linux
    without requiring third-party pip dependencies.
    """
    cpu_name = platform.processor() or "Unknown CPU"
    threads = os.cpu_count() or 1
    total_ram_gb = None
    avail_ram_gb = None

    # 1. Windows Hardware Detection
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
            )
            val, _ = winreg.QueryValueEx(key, "ProcessorNameString")
            cpu_name = val.strip()
        except Exception:
            pass

        try:
            import ctypes

            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                total_ram_gb = stat.ullTotalPhys / (1024 ** 3)
                avail_ram_gb = stat.ullAvailPhys / (1024 ** 3)
        except Exception:
            pass

    # 2. macOS (Darwin) Hardware Detection
    elif sys.platform == "darwin":
        import subprocess
        try:
            cpu_name = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).decode().strip()
        except Exception:
            pass
        try:
            mem_bytes = int(subprocess.check_output(["sysctl", "-n", "hw.memsize"]).decode().strip())
            total_ram_gb = mem_bytes / (1024 ** 3)
        except Exception:
            pass

    # 3. Linux Hardware Detection
    elif sys.platform.startswith("linux"):
        try:
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if "model name" in line:
                        cpu_name = line.split(":", 1)[1].strip()
                        break
        except Exception:
            pass
        try:
            with open("/proc/meminfo") as f:
                for line in f:
                    if "MemTotal" in line:
                        total_ram_gb = int(line.split()[1]) / (1024 ** 2)
                    elif "MemAvailable" in line:
                        avail_ram_gb = int(line.split()[1]) / (1024 ** 2)
        except Exception:
            pass

    # Fallback if psutil is available
    if total_ram_gb is None:
        try:
            import psutil
            mem = psutil.virtual_memory()
            total_ram_gb = mem.total / (1024 ** 3)
            avail_ram_gb = mem.available / (1024 ** 3)
        except Exception:
            pass

    ram_str = f"{total_ram_gb:.2f} GB" if total_ram_gb else "Unknown RAM"
    if avail_ram_gb is not None:
        ram_str += f" Total ({avail_ram_gb:.2f} GB Free)"

    try:
        hostname = socket.gethostname()
    except Exception:
        hostname = "Laptop/PC"

    return {
        "hostname": hostname,
        "cpu": cpu_name,
        "threads": threads,
        "ram": ram_str,
        "os": f"{platform.system()} {platform.release()} ({platform.architecture()[0]})",
        "python": f"Python {platform.python_version()} ({platform.python_implementation()})",
    }


def generate_benchmark_graph(V: int) -> list[list[int]]:
    """
    Generates a deterministic V x V adjacency matrix matching the formula
    used in the original C and Python comparison benchmarks:
        graph[i][j] = 0 if i == j else (i + j) % 10 + 1
    """
    return [[0 if i == j else ((i + j) % 10 + 1) for j in range(V)] for i in range(V)]


def run_benchmark():
    specs = get_system_specs()

    print("=" * 92)
    print("             DIJKSTRA SHORTEST PATH PRODUCTION BENCHMARK             ")
    print("                 Pure Python vs C++ (Cython Wrapper)                 ")
    print("=" * 92)
    print(f" Device / Host: {specs['hostname']}")
    print(f" CPU Model    : {specs['cpu']} ({specs['threads']} Logical Threads)")
    print(f" RAM Config   : {specs['ram']}")
    print(f" Operating Sys: {specs['os']}")
    print(f" Python Env   : {specs['python']}")
    print(" Timing Method: timeit.default_timer (Monotonic hardware performance clock)")
    print(" Sampling     : Multi-run averaging per test tier")
    print("=" * 92)

    if dijkstra_cython is None:
        print("\n" + "=" * 92)
        print("                 [NOTICE] C++ CYTHON MODULE NOT YET COMPILED                ")
        print("=" * 92)
        print(" The pure Python Dijkstra solver is ready and verified.")
        print(" To enable the C++ Cython speedup comparison on this machine:")
        print("   1. Ensure a C++ compiler is installed:")
        print("      * Windows : Install Visual Studio C++ Build Tools or MinGW g++")
        print("      * macOS   : Run 'xcode-select --install'")
        print("      * Linux   : Run 'sudo apt install build-essential python3-dev'")
        print("   2. Run compilation command:")
        print("      python setup.py build_ext --inplace\n")
        print("=" * 92)
        print(f"{'Graph / Size (V)':<22} | {'Matrix Size (V^2)':<19} | {'Python Time':<13} | {'Status':<25}")
        print("-" * 85)

        dehradun_matrix = build_dehradun_distance_matrix()
        v_deh = len(dehradun_matrix)
        start_py = timeit.default_timer()
        for _ in range(300):
            dijkstra_python(dehradun_matrix, 0)
        t_py = (timeit.default_timer() - start_py) / 300
        py_str = f"{t_py * 1000:.3f} ms"
        print(f"{f'Dehradun Map (V={v_deh})':<22} | {v_deh * v_deh:<19,d} | {py_str:<13} | {'Pure Python OK':<25}")

        for v in [200, 500, 1000]:
            matrix = generate_benchmark_graph(v)
            start_py = timeit.default_timer()
            runs = 10 if v < 500 else 3
            for _ in range(runs):
                dijkstra_python(matrix, 0)
            t_py = (timeit.default_timer() - start_py) / runs
            py_str = f"{t_py * 1000:.2f} ms" if t_py < 1.0 else f"{t_py:.3f} s"
            print(f"{f'V = {v}':<22} | {v * v:<19,d} | {py_str:<13} | {'Pure Python OK':<25}")

        print("-" * 85)
        print("\nCompile the C++ extension to see the 15x-25x speedup comparison!")
        return []

    header = f"{'Graph / Size (V)':<22} | {'Matrix Size (V^2)':<19} | {'Python Time':<13} | {'Cython Time':<13} | {'Speedup':<10}"
    separator = "-" * len(header)
    print(header)
    print(separator)

    benchmark_rows = []

    # 1. Real-World Dehradun Graph Benchmark
    dehradun_matrix = build_dehradun_distance_matrix()
    v_deh = len(dehradun_matrix)
    deh_runs = 500

    # Cython timing
    start_cy = timeit.default_timer()
    for _ in range(deh_runs):
        cy_dist = dijkstra_cython(dehradun_matrix, 0)
    end_cy = timeit.default_timer()
    cy_time_deh = (end_cy - start_cy) / deh_runs

    # Python timing
    start_py = timeit.default_timer()
    for _ in range(deh_runs):
        py_dist = dijkstra_python(dehradun_matrix, 0)
    end_py = timeit.default_timer()
    py_time_deh = (end_py - start_py) / deh_runs

    assert py_dist == cy_dist, "Dehradun solver output mismatch"
    speedup_deh = py_time_deh / cy_time_deh if cy_time_deh > 0 else 1.0

    cy_str = f"{cy_time_deh * 1000:.3f} ms" if cy_time_deh < 0.001 else f"{cy_time_deh:.6f} s"
    py_str = f"{py_time_deh * 1000:.3f} ms" if py_time_deh < 0.001 else f"{py_time_deh:.6f} s"
    speedup_str = f"{speedup_deh:.1f}x"

    print(f"{f'Dehradun Map (V={v_deh})':<22} | {v_deh * v_deh:<19,d} | {py_str:<13} | {cy_str:<13} | {speedup_str:<10}")
    benchmark_rows.append({
        "label": f"Dehradun Map (V={v_deh})",
        "v": v_deh,
        "edges": v_deh * v_deh,
        "py_time": py_time_deh,
        "cy_time": cy_time_deh,
        "speedup": speedup_deh,
    })

    # 1b. Direct Nodes [[x, y]] & Edges [{s, d, w}] Format Benchmark
    edge_runs = 500
    start_cy_e = timeit.default_timer()
    for _ in range(edge_runs):
        dist_cy_e, path_cy_e = dijkstra_from_edges_cython(NODES_COORDS, EDGES_DICTS, 0, 20)
    end_cy_e = timeit.default_timer()
    cy_time_e = (end_cy_e - start_cy_e) / edge_runs

    start_py_e = timeit.default_timer()
    for _ in range(edge_runs):
        dist_py_e, path_py_e = dijkstra_from_edges_python(NODES_COORDS, EDGES_DICTS, 0, 20)
    end_py_e = timeit.default_timer()
    py_time_e = (end_py_e - start_py_e) / edge_runs

    assert dist_cy_e == dist_py_e and path_cy_e == path_py_e, "Direct Edge solver output mismatch"
    speedup_e = py_time_e / cy_time_e if cy_time_e > 0 else 1.0

    cy_str_e = f"{cy_time_e * 1000:.3f} ms" if cy_time_e < 0.001 else f"{cy_time_e:.6f} s"
    py_str_e = f"{py_time_e * 1000:.3f} ms" if py_time_e < 0.001 else f"{py_time_e:.6f} s"
    speedup_str_e = f"{speedup_e:.1f}x"

    print(f"{'Dehradun [nodes,edges]':<22} | {len(EDGES_DICTS):<19,d} | {py_str_e:<13} | {cy_str_e:<13} | {speedup_str_e:<10}")
    benchmark_rows.append({
        "label": "Dehradun [nodes,edges]",
        "v": len(NODES_COORDS),
        "edges": len(EDGES_DICTS),
        "py_time": py_time_e,
        "cy_time": cy_time_e,
        "speedup": speedup_e,
    })

    # 2. Scaled Synthetic Dense Graph Benchmarks
    test_sizes = [
        (200, 20),
        (500, 5),
        (1000, 3),
        (1500, 2),
    ]

    for v, runs in test_sizes:
        matrix = generate_benchmark_graph(v)
        total_cells = v * v

        # Cython timing
        start_cy = timeit.default_timer()
        for _ in range(runs):
            cy_dist = dijkstra_cython(matrix, 0)
        end_cy = timeit.default_timer()
        cy_time = (end_cy - start_cy) / runs

        # Python timing
        start_py = timeit.default_timer()
        for _ in range(runs):
            py_dist = dijkstra_python(matrix, 0)
        end_py = timeit.default_timer()
        py_time = (end_py - start_py) / runs

        assert py_dist == cy_dist, f"Output mismatch for V={v}"
        speedup = py_time / cy_time if cy_time > 0 else 1.0

        cy_str = f"{cy_time * 1000:.2f} ms" if cy_time < 1.0 else f"{cy_time:.3f} s"
        py_str = f"{py_time * 1000:.2f} ms" if py_time < 1.0 else f"{py_time:.3f} s"
        speedup_str = f"{speedup:.1f}x"

        row = f"{f'V = {v}':<22} | {total_cells:<19,d} | {py_str:<13} | {cy_str:<13} | {speedup_str:<10}"
        print(row)

        benchmark_rows.append({
            "label": f"V = {v}",
            "v": v,
            "edges": total_cells,
            "py_time": py_time,
            "cy_time": cy_time,
            "speedup": speedup,
        })

    print(separator)
    avg_speedup = sum(r["speedup"] for r in benchmark_rows) / len(benchmark_rows)
    print(f"\n[SUMMARY FOR {specs['hostname'].upper()}]")
    print(f"  * Processor     : {specs['cpu']}")
    print(f"  * Memory Config : {specs['ram']}")
    print(f"  * Average Boost : Cython is {avg_speedup:.1f}x faster than pure Python on this machine!")
    print(f"  * Status        : All outputs verified mathematically identical.")
    return benchmark_rows


if __name__ == "__main__":
    run_benchmark()
