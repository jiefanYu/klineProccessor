from setuptools import setup, find_packages

setup(
    name="kline-pipeline",
    version="0.1.0",
    description="A scalable, resumable and exactly-once A-share K-line generator.",
    author="Jiefan YU",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3",
        "dask>=2022.0.0",
        "pyarrow>=7.0.0"
    ],
    entry_points={
        'console_scripts': [
            'kline-pipeline = main:main'
        ]
    },
    python_requires='>=3.7',
)