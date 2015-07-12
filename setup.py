try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Solver for sudoku puzzles',
    'author': 'luxmeter',
    'url': 'https://github.com/luxmeter/sudokusolver',
    'download_url': 'https://github.com/luxmeter/sudokusolver',
    'version': '0.1',
    'entry_points': {
        'console_scripts': [
            'sudokusolver = sudokusolver.__main__:main'
        ]
    },
    'test_suite': 'tests',
    # 'install_requires': ['nose'],
    'packages': ['sudokusolver'],
    'scripts': [],
    'name': 'sudokusolver'
}

setup(**config)
