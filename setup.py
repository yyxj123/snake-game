from setuptools import setup, find_packages

setup(
    name="super-snake",
    version="1.0.0",
    description="🐍 A beautiful and feature-rich Snake game",
    author="小吴虾",
    author_email="example@email.com",
    url="https://github.com/yourusername/snake-game",
    packages=find_packages(),
    install_requires=[
        'pygame>=2.0.0',
    ],
    entry_points={
        'console_scripts': [
            'super-snake=main:run',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
