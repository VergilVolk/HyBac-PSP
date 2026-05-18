from setuptools import setup, find_packages

setup(
    name="HyBac-PSP",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "biopython",
        "numpy",
        "pandas",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "hybac=api:main",
        ],
    },
)