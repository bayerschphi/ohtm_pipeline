from setuptools import setup, find_packages

setup(
    name="ohtm_pipeline",
    version="0.8.0",
    description="Kurzbeschreibung des Projekts",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Philipp Bayerschmidt",
    author_email="philipp.bayerschmidt@fernuni-hagen.de",
    url="https://github.com/bayerschphi/ohtm_pipeline",
    packages=find_packages(where="ohtm_pipeline"),  # nur den inneren Ordner durchsuchen
    package_dir={"": "ohtm_pipeline"},             # Mapping: Paketname -> Ordner
    install_requires=[
        "pandas",
        "matplotlib",
        "plotly",
        "scikit-learn",
        "nltk"
    ],
)