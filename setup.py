"""Setup configuration for Hybrid dialectical framework"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hybrid-dialectical",
    version="0.1.0",
    author="Hybrid Project",
    description="Dialectical reasoning framework with PSIP compression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.4.0",
        "pytest-cov>=4.1.0",
        "pydantic>=2.5.0",
        "numpy>=1.24.0",
        "scikit-learn>=1.3.0",
        "click>=8.1.0",
        "rich>=13.7.0",
        "prompt-toolkit>=3.0.43",
        "pyyaml>=6.0.1",
        "jsonschema>=4.20.0",
    ],
    extras_require={
        "dev": [
            "ruff>=0.1.0",
            "black>=23.12.0",
            "mypy>=1.7.0",
            "ipython>=8.18.0",
            "jupyter>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "hybrid-dialectical=cli.dialectical_engine:main",
            "hybrid-troupe=cli.troupe_manager:main",
            "hybrid-psip=psip.compress:main",
        ],
    },
)
