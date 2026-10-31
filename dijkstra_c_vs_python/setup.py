import os
import sys
import shutil
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize

# Ensure 64-bit LLVM-MinGW compiler takes priority if on Windows
winget_llvm = os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\MartinStorsjo.LLVM-MinGW.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\llvm-mingw-20261020-ucrt-x86_64\bin"
)
if os.path.isdir(winget_llvm):
    clean_paths = [p for p in os.environ.get("PATH", "").split(os.pathsep) if "C:\\MinGW" not in p]
    os.environ["PATH"] = winget_llvm + os.pathsep + os.pathsep.join(clean_paths)

class SmartBuildExt(build_ext):
    """
    Custom build_ext to automatically handle compilers on Windows, Linux, and macOS.
    Only selects mingw32 if gcc/g++ is actually found and MSVC cl is not.
    """
    def finalize_options(self):
        super().finalize_options()
        if sys.platform == "win32" and self.compiler is None:
            has_cl = bool(shutil.which("cl"))
            has_gcc = bool(shutil.which("gcc") or shutil.which("g++"))
            if has_gcc and not has_cl:
                self.compiler = "mingw32"

extra_compile_args = ["-O3", "-std=c++17"]
extra_link_args = []

if sys.platform == "win32":
    if shutil.which("cl") and not shutil.which("g++"):
        extra_compile_args = ["/O2", "/std:c++17"]
    else:
        extra_link_args = ["-static"]

ext_modules = [
    Extension(
        name="dijkstra_fast_solver.dijkstra_wrapper",
        sources=[
            "cython_wrapper/dijkstra_wrapper.pyx",
            "cpp/dijkstra.cpp",
        ],
        include_dirs=["cpp", "cython_wrapper"],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name="dijkstra-fast-solver",
    version="0.1.0",
    description="Blazing fast C++ Dijkstra shortest path solver wrapped in Cython",
    packages=find_packages(),
    ext_modules=cythonize(
        ext_modules,
        language_level="3",
        compiler_directives={"boundscheck": False, "wraparound": False},
    ),
    cmdclass={"build_ext": SmartBuildExt},
)
