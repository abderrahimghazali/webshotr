from setuptools import setup, find_packages

try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "A simple and fast website screenshot tool"

setup(
    name="webshotr",
    version="1.0.0",
    author="AbderrahimGHAZALI",
    author_email="ghazali.abderrahim1@gmail.com",
    description="A simple and fast website screenshot tool - WebShotr",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abderrahimghazali/webshotr",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    keywords="screenshot, web, automation, playwright, browser, capture",
    python_requires=">=3.7",
    install_requires=[
        "playwright>=1.40.0",
        "Pillow>=9.0.0",
        "click>=8.0.0",
        "aiofiles>=22.0.0",
    ],
    entry_points={
        "console_scripts": [
            "webshotr=webshotr.cli:main",
        ],
    },
)