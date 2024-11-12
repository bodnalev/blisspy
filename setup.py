from setuptools import setup, Extension
from Cython.Build import cythonize
import os

current_dir = os.getcwd()
bliss_include_dir = os.path.join(current_dir, 'include')
bliss_src_dir = os.path.join(current_dir, 'src')

bliss_source_files = [
    os.path.join('src', filename)
    for filename in os.listdir(bliss_src_dir)
    if filename.endswith('.cc')
]

with open("README.md", "r") as fp:
    long_desc = fp.read()

extensions = [
    Extension(
        name="blisspy",
        sources=["blisspy.pyx"] + bliss_source_files,
        language="c++",
        include_dirs=[
            bliss_include_dir,
            os.path.join(bliss_include_dir, 'bliss'),
        ],
        extra_compile_args=[
            '-std=c++11',
            '-O3',
            #'-g', probably not needed to debug this wrapper
            '-Wall',
            '-Wextra',
            '--pedantic',
            '-fPIC',
        ],
        define_macros=[
            ('NDEBUG', None),
        ],
    )
]

setup(
    name="blisspy",
    version="0.1",
    author="Levente Bodnar",
    author_email="bodnalev@gmail.com",
    description="Python wrapper for the Bliss graph library",
    long_description_content_type='text/markdown',
    long_description=long_desc,
    license="GNU",
    packages=[''],
    py_modules=['blisspy'],
    package_data={'': ['*.pxd']},
    include_package_data=True,
    ext_modules=cythonize(extensions),
)
