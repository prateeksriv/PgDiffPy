from setuptools import setup, find_packages

setup(
    name='PgDiffPy',
    version='1.0.0',
    author='Prateek',
    author_email='for.groups+GITHUB@gmail.com',
    description='A Python-based tool for comparing PostgreSQL database schemas.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Dancer3809/PgDiffPy',
    packages=find_packages(),
    install_requires=[
        'sqlparse>=0.1.8',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'pgdiff=PgDiff:main',
        ],
    },
)
