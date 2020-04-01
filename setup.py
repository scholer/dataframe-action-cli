from setuptools import setup
import os

PROJECT_ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file

try:
    with open(os.path.join(PROJECT_ROOT_DIR, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except IOError:
    long_description = """
DataFrame Action CLI (dataframe-action-cli).

A `find`-inspired CLI for manipulating tabular data using Pandas DataFrames.

Load csv files, sort and filter rows, add new columns, and output the updated data to files
from the command line.

See `README.md` for usage.

"""

setup(
    name='dataframe-action-cli',
    version='2020.1.15',
    packages=['dataframe_action_cli'],
    url='https://github.com/scholer/dataframe-action-cli',
    license='GPLv3',
    author='Rasmus S. Sorensen',
    author_email='rasmusscholer@gmail.com',
    description='CLI for manipulating tabular data using Pandas DataFrames, using "Action CLI"-style declarations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['Pandas', 'DataFrame', 'CSV', 'CLI', 'Application'],
    entry_points={
        'console_scripts': [
            # Action CLI entry point:
            'dataframe-action-cli=dataframe_action_cli.cli:action_cli',
        ],
        # 'gui_scripts': [
        # ]
    },
    python_requires='>=3.6',  # Type-hints, f-strings,
    install_requires=[
        'pandas',
    ],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',

        'Topic :: Scientific/Engineering',

        # Pick your license as you wish (should match 'license' above)
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

        'Operating System :: MacOS',
        'Operating System :: Microsoft',
        'Operating System :: POSIX :: Linux',
    ],
)
