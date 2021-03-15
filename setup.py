import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="radioactivedecay",
    version="0.2.3",
    author="Alex Malins",
    author_email="radioactivedecay@REMOVETHISalexmalins.com",
    license="MIT",
    description="A Python package for radioactive decay calculations that supports 1252 radionuclides, decay chains, branching, and metastable states.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexmalins/radioactivedecay",
    project_urls={
        "Bug Tracker": "https://github.com/alexmalins/radioactivedecay/issues",
        "Documentation": "https://alexmalins.com/radioactivedecay",
        "Source Code": "https://github.com/alexmalins/radioactivedecay",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Education ",
    ],
    install_requires=[
        "matplotlib",
        "numpy",
        "scipy",
        "sympy",
        "importlib_resources; python_version<'3.7'",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    package_data={
        "": [
            "icrp107/decay_data.npz",
            "icrp107/c_scipy.npz",
            "icrp107/c_inv_scipy.npz",
            "icrp107/decay_consts_sympy.pickle",
            "icrp107/c_sympy.pickle",
            "icrp107/c_inv_sympy.pickle",
            "icrp107/year_conversion_sympy.pickle",
        ]
    },
)
