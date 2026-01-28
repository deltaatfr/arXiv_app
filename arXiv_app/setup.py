from setuptools import setup, find_packages

setup(
    name="arxiv-tracker",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "arxiv_tracker": ["data/**/*"]
    },
    install_requires=[
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.2",
        "tqdm>=4.66.1",
        "psutil>=5.9.6",
        "dashscope>=1.17.0",
        "PyPDF2>=3.0.1",
        "markdown>=3.4.4"
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.11.0",
            "flake8>=6.1.0",
            "isort>=5.12.0"
        ]
    },
    entry_points={
        "console_scripts": [
            "arxiv-tracker=arxiv_tracker.cli:main",
        ],
    },
    author="arXiv Tracker Team",
    author_email="contact@arxiv-tracker.example",
    description="arXiv论文跟踪和分析系统",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/arxiv-tracker",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Researchers",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    python_requires=">=3.7"
)
