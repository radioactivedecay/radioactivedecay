import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="radioactivedecay", # Replace with your own username
    version="0.0.1",
    author="Alex Malins",
    author_email="pypi@REMOVETHISalexmalins.com",
    license='MIT',
    description="radioactivedecay is a Python package for performing radioactive decay calculations. It supports 1252 radionuclides, including calculating full decay chains and branching.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexmalins/radioactivedecay",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["scipy", "numpy", "importlib_resources ; python_version<'3.7'"],
    python_requires='>=3.6',
    packages=setuptools.find_packages(),
    package_data={'': ['icrp107/*.csv', 'icrp107/*.npz']},
)