from setuptools import setup

setup(
    name='main',
    version='0.1.0',
    py_modules=['main'],
    install_requires=[
        'certifi==2025.1.31',
        'charset-normalizer==3.4.1',
        'click==8.1.8',
        'dotenv==0.9.9',
        'idna==3.10',
        'python-dotenv==1.0.1',
        'redis==5.2.1',
        'requests==2.32.3',
        'setuptools==78.1.0',
        'spotipy==2.25.1',
        'tqdm==4.67.1',
        'urllib3==2.3.0',
    ],
    entry_points={
        'console_scripts': [
            'main = main:cli',
        ],
    },
)
