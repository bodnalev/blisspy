from setuptools import setup, Extension
from Cython.Build import cythonize
import os, glob

bliss_source_files = glob.glob("src/*.cc")

with open("README.md", "r") as fp:
    long_desc = fp.read()

setup(
    name="blisspy",
    version="0.1",
    author="Levente Bodnar",
    author_email="bodnalev@gmail.com",
    description="Python wrapper for the Bliss graph library",
    long_description_content_type='text/markdown',
    long_description=long_desc,
    license="GNU",
    packages=["blisspy"],
    package_data={"blisspy": ["*.pxd"]},
    include_package_data=True,
    ext_modules=cythonize([
        Extension(
            name="blisspy",
            sources=["blisspy/__init__.pyx"] + bliss_source_files,
            language="c++",
            include_dirs=["include"],
            extra_compile_args=['-std=c++11', '-O3', '-fPIC'],
            define_macros=[('NDEBUG', None)]
        )
    ], compiler_directives={"language_level": "3"}),
    install_requires=["Cython", "cysignals"]
)

