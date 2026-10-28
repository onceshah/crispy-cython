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
    Custom build_ext to automatically select mingw32 on Windows
    when MSVC cl.exe is not available in PATH.
    """
    def finalize_options(self):
        super().finalize_options()
        if sys.platform == "win32" and self.compiler is None:
            if not shutil.which("cl"):
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
        name="tsp_fast_solver.tsp_wrapper",
        sources=[
            "cython_wrapper/tsp_wrapper.pyx",
            "cpp/tsp.cpp",
        ],
        include_dirs=["cpp", "cython_wrapper"],
        language="c++",
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    ),
]

setup(
    name="tsp-fast-solver",
    version="0.1.0",
    packages=find_packages(),
    ext_modules=cythonize(
        ext_modules,
        language_level="3",
        compiler_directives={"boundscheck": False, "wraparound": False},
    ),
    cmdclass={"build_ext": SmartBuildExt},
)
