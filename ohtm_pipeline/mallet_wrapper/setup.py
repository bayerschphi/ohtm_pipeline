from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy

# Liste der Cython-Module, die kompiliert werden sollen
extensions = [
    Extension(
        "ohtm_pipeline.mallet_wrapper.matutils",
        ["ohtm_pipeline/mallet_wrapper/matutils.pyx"],  # falls es nur .py gibt, umbenennen in .pyx
        include_dirs=[numpy.get_include()],
    ),
]

setup(
    name="ohtm_mallet_wrapper",
    ext_modules=cythonize(extensions, language_level="3"),
)