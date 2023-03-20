from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules=cythonize('DMA_cell.pyx')
)
