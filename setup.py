import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xuerui-stat",
    version="0.0.6",
    author="Xuerui Yang",
    author_email="xuerui-yang@outlook.com",
    description="A statistical package to manage and analyse data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=" https://github.com/Xuerui-Yang/xuerui-stat",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
