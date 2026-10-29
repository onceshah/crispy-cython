import matplotlib.pyplot as plt
import numpy as np

# Set high-resolution professional dark theme
plt.style.use('dark_background')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.8), dpi=300)
fig.patch.set_facecolor('#0B0F19')
for ax in (ax1, ax2):
    ax.set_facecolor('#111827')

# Data
graph_sizes = ['N = 8\n(5,040 routes)', 'N = 10\n(362,880 routes)', 'N = 11\n(3,628,800 routes)']
py_times_ms = [1.65, 145.2, 1610.0]     # in milliseconds
cy_times_ms = [0.021, 1.39, 14.30]      # in milliseconds
speedups = [78.6, 104.5, 112.6]

x = np.arange(len(graph_sizes))
width = 0.35

# Plot 1: Execution Time (Log Scale)
rects1 = ax1.bar(x - width/2, py_times_ms, width, label='Pure Python (itertools)', color='#F43F5E', edgecolor='#FDA4AF', linewidth=1.2)
rects2 = ax1.bar(x + width/2, cy_times_ms, width, label='C++ with Cython (std::next_permutation)', color='#06B6D4', edgecolor='#67E8F9', linewidth=1.2)

ax1.set_yscale('log')
ax1.set_ylabel('Execution Time (ms, Log Scale)', fontsize=12, fontweight='bold', color='#E2E8F0')
ax1.set_title('Execution Time Comparison (Lower is Better)', fontsize=13.5, fontweight='bold', pad=15, color='#F8FAFC')
ax1.set_xticks(x)
ax1.set_xticklabels(graph_sizes, fontsize=11, color='#CBD5E1')
ax1.legend(frameon=True, facecolor='#1E293B', edgecolor='#334155', fontsize=10)
ax1.grid(axis='y', linestyle='--', alpha=0.25, color='#94A3B8')
ax1.tick_params(colors='#94A3B8')

# Value labels on Plot 1
for rect in rects1:
    h = rect.get_height()
    label = f"{h:.2f} ms" if h < 1000 else f"{h/1000:.2f} s"
    ax1.annotate(label, xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                 fontsize=9.5, fontweight='bold', color='#FDA4AF')

for rect in rects2:
    h = rect.get_height()
    label = f"{h:.3f} ms" if h < 1.0 else f"{h:.2f} ms"
    ax1.annotate(label, xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                 fontsize=9.5, fontweight='bold', color='#67E8F9')

# Plot 2: Speedup Multiplier Per N
rects3 = ax2.bar(x, speedups, width=0.45, color='#10B981', edgecolor='#34D399', linewidth=1.2)
ax2.set_ylabel('Speedup Factor (x Times Faster)', fontsize=12, fontweight='bold', color='#E2E8F0')
ax2.set_title('Acceleration Factor Per N (Higher is Better)', fontsize=13.5, fontweight='bold', pad=15, color='#F8FAFC')
ax2.set_xticks(x)
ax2.set_xticklabels(graph_sizes, fontsize=11, color='#CBD5E1')
ax2.grid(axis='y', linestyle='--', alpha=0.25, color='#94A3B8')
ax2.tick_params(colors='#94A3B8')

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f"{h:.1f}x FASTER", xy=(rect.get_x() + rect.get_width()/2, h),
                 xytext=(0, 6), textcoords="offset points", ha='center', va='bottom',
                 fontsize=10.5, fontweight='bold', color='#A7F3D0')

# Overall Figure Title
fig.suptitle('Traveling Salesperson Problem (TSP): Pure Python vs C++ Cython',
             fontsize=16.5, fontweight='heavy', color='#F8FAFC', y=0.98)

# Hardware and Methodology Caption
plt.figtext(0.5, 0.045,
            'Hardware: Intel Core i7-13700HX (16 Cores, 24 Threads) | 16 GB RAM | Windows 11 (64-bit) | Python 3.13.7',
            ha='center', fontsize=9.5, color='#E2E8F0', fontweight='medium')
plt.figtext(0.5, 0.015,
            'Timing: timeit.default_timer() monotonic QPC clock (Multi-run sample averages) | PyPI: pip install tsp-fast-solver',
            ha='center', fontsize=9, color='#94A3B8', style='italic')

plt.tight_layout(rect=[0, 0.06, 1, 0.94])
plt.savefig('d:/UPES/SEM 7/Cython/tsp_benchmark_comparison.png', dpi=300, facecolor=fig.get_facecolor())
print('Chart updated successfully!')
