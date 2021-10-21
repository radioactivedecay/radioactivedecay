import setuptools

project = "radioactivedecay"

with open(f"{project}/__init__.py", "r") as file:
    for line in file:
        if line.startswith("__version__"):
            version = line.strip().split()[-1][1:-1]
            break

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name=project,
    version=version,
    author="Alex Malins",
    author_email="radioactivedecay@REMOVETHISalexmalins.com",
    license="MIT, ICRP-07, AMDC",
    description="A Python package for radioactive decay modelling that supports 1252 radionuclides, decay chains, branching, and metastable states.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/radioactivedecay/radioactivedecay",
    project_urls={
        "Bug Tracker": "https://github.com/radioactivedecay/radioactivedecay/issues",
        "Discussions": "https://github.com/radioactivedecay/radioactivedecay/discussions",
        "Documentation": "https://radioactivedecay.github.io",
        "Source Code": "https://github.com/radioactivedecay/radioactivedecay",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering",
        "Topic :: Education",
    ],
    install_requires=[
        "matplotlib",
        "networkx",
        "numpy",
        "scipy",
        "sympy",
        "importlib_resources; python_version<'3.7'",
    ],
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    package_data={
        "": [
            "icrp107_ame2020_nubase2020/atomic_masses_sympy_1.8.pickle",
            "icrp107_ame2020_nubase2020/atomic_masses_sympy_1.9.pickle",
            "icrp107_ame2020_nubase2020/decay_data.npz",
            "icrp107_ame2020_nubase2020/c_scipy.npz",
            "icrp107_ame2020_nubase2020/c_inv_scipy.npz",
            "icrp107_ame2020_nubase2020/decay_consts_sympy_1.8.pickle",
            "icrp107_ame2020_nubase2020/decay_consts_sympy_1.9.pickle",
            "icrp107_ame2020_nubase2020/c_sympy_1.8.pickle",
            "icrp107_ame2020_nubase2020/c_sympy_1.9.pickle",
            "icrp107_ame2020_nubase2020/c_inv_sympy_1.8.pickle",
            "icrp107_ame2020_nubase2020/c_inv_sympy_1.9.pickle",
            "icrp107_ame2020_nubase2020/year_conversion_sympy_1.8.pickle",
            "icrp107_ame2020_nubase2020/year_conversion_sympy_1.9.pickle",
        ]
    },
)
