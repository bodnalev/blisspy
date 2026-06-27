from pathlib import Path
import glob

from setuptools import setup, Extension, find_packages
from Cython.Build import cythonize

try:
    from cysignals import get_include as cysignals_get_include
except ImportError:
    cysignals_get_include = None


ROOT = Path(__file__).parent

bliss_source_files = sorted(glob.glob("src/*.cc"))

with open(ROOT / "README.md", "r", encoding="utf-8") as fp:
    long_desc = fp.read()

include_dirs = ["include"]

if cysignals_get_include is not None:
    include_dirs.append(cysignals_get_include())


extensions = [
    Extension(
        name="blisspy._core",
        sources=["blisspy/_core.pyx"] + bliss_source_files,
        language="c++",
        include_dirs=include_dirs,
        extra_compile_args=["-std=c++11", "-O3", "-fPIC"],
        define_macros=[("NDEBUG", None)],
    )
]


setup(
    name="blisspy",
    version="0.1",
    author="Levente Bodnar",
    author_email="bodnalev@gmail.com",
    description="Python wrapper for the Bliss graph library",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    license="GNU",

    packages=find_packages(include=["blisspy", "blisspy.*"]),

    package_data={
        "blisspy": ["*.pxd", "*.pyx", "*.cpp"],
    },
    include_package_data=True,

    ext_modules=cythonize(
        extensions,
        compiler_directives={"language_level": "3"},
    ),

    install_requires=[
        "cysignals",
    ],

    zip_safe=False,
)
