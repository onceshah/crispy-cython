import os
import sys
import shutil
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

# Ensure 64-bit LLVM-MinGW compiler takes priority on Windows if present
winget_llvm = os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20261020-ucrt-x86_64\bin"
)
if os.path.isdir(winget_llvm):
    clean_paths = [p for p in os.environ.get("PATH", "").split(os.pathsep) if "C:\\MinGW" not in p]
    os.environ["PATH"] = winget_llvm + os.pathsep + os.pathsep.join(clean_paths)

class SmartBuildExt(build_ext):
    """
    Custom build_ext to automatically handle compilers on Windows, Linux, and macOS.
    Automatically selects mingw32 on Windows when MSVC cl is not available.
    Falls back gracefully if compiler execution fails.
    """
    def finalize_options(self):
        super().finalize_options()
        if sys.platform == "win32" and self.compiler is None:
            has_cl = bool(shutil.which("cl"))
            has_gcc = bool(shutil.which("gcc") or shutil.which("g++"))
            if has_gcc and not has_cl:
                self.compiler = "mingw32"

    def run(self):
        try:
            super().run()
        except Exception as e:
            print(f"WARNING: Building C++ Cython extensions failed: {e}")
            print("crispy-cython will install with pure Python algorithmic fallbacks.")

extra_compile_args = ["-O3", "-std=c++17"]
extra_link_args = []

if sys.platform == "win32":
    if shutil.which("cl") and not shutil.which("g++"):
        extra_compile_args = ["/O2", "/std:c++17"]
    else:
        extra_link_args = ["-static"]

try:
    from Cython.Build import cythonize
    ext_modules = cythonize(
        [
            Extension(
                name="crispy_cython.dijkstra.dijkstra_wrapper",
                sources=[
                    "crispy_cython/dijkstra/dijkstra_wrapper.pyx",
                    "crispy_cython/dijkstra/cpp/dijkstra.cpp",
                ],
                include_dirs=["crispy_cython/dijkstra/cpp", "crispy_cython/dijkstra"],
                language="c++",
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args,
            ),
            Extension(
                name="crispy_cython.tsp.tsp_wrapper",
                sources=[
                    "crispy_cython/tsp/tsp_wrapper.pyx",
                    "crispy_cython/tsp/cpp/tsp.cpp",
                ],
                include_dirs=["crispy_cython/tsp/cpp", "crispy_cython/tsp"],
                language="c++",
                extra_compile_args=extra_compile_args,
                extra_link_args=extra_link_args,
            ),
        ],
        language_level="3",
        compiler_directives={"boundscheck": False, "wraparound": False},
    )
except ImportError:
    ext_modules = []

setup(
    packages=find_packages(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": SmartBuildExt},
)
