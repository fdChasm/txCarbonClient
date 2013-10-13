import setuptools

setuptools.setup(
    name="txCarbonClient",
    version="0.1",
    packages=["txCarbonClient"],
    package_dir={'' : 'src'},
    install_requires=["twisted"],
    author="Chasm",
    author_email="fd.chasm@gmail.com",
    url="https://github.com/fdChasm/txCarbonClient",
    license="MIT",
    description="A simple Twisted client for reporting metrics to Carbon.",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
    ],
)
