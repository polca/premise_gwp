from setuptools import setup

v_temp = {}
with open("premise_gwp/version.py") as fp:
    exec(fp.read(), v_temp)
version = ".".join((str(x) for x in v_temp["version"]))


setup(
    name="premise_gwp",
    version=version,
    packages=[
        "premise_gwp",
    ],
    author="Romain Sacchi",
    author_email="romain.sacchi@psi.ch",
    license="BSD 3-clause",
    package_data={"premise_gwp": ["data/*.xlsx", "data/*.json"]},
    install_requires=[
        "bw2io",
        "bw2data",
        "requests",
    ],
    url="https://github.com/romainsacchi/premise_gwp",
    long_description_content_type="text/markdown",
    long_description=open("README.md").read(),
    description="Import IPCC's GWP100a method, with biogenic CO2 CFs, into Brightway2",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
