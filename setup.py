from setuptools import setup, Extension
from Cython.Build import cythonize
import os
import glob

bliss_include_dir = 'include'

bliss_src_dir = 'src'

# Use relative paths for source files
bliss_source_files = glob.glob(os.path.join(bliss_src_dir, '*.cc'))
#bliss_source_files = [
#    os.path.join('src', filename)
#    for filename in os.listdir(bliss_src_dir)
#    if filename.endswith('.cc')
#]

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
    package_data={'': ['*.pxd']},
    include_package_data=True,
    ext_modules=cythonize(extensions, compiler_directives={"language_level": "3"})
)
