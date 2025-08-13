from setuptools import setup, find_packages

setup(
    name="Oral History Topic Modeling Pipeline",
    version="0.8.0",
    description="Kurzbeschreibung des Projekts",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Philipp Bayerschmidt",
    author_email="philipp.bayerschmidt@fernuni-hagen.de",
    url="https://github.com/bayerschphi/ohtm_pipeline",
    packages=find_packages() + ["ohtm"],  # explicitly include top-level ohtm
    package_dir={"ohtm": "ohtm_pipeline/ohtm"}  # map 'ohtm' to that subfolder
)
