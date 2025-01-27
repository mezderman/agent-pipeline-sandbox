from setuptools import setup, find_packages

setup(
    name="agent_pipeline_sandbox",
    version="0.1",
    packages=find_packages(include=['*']),
    package_dir={"": "."},
)
