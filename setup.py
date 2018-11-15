import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gatecoin_api",
    version="1.0.0",
    author="Ahmed Belal",
    author_email="contact@gatecoin.com",
    description="A simple GateCoin REST API client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gatecoin/api-gatecoin-python",
    packages=setuptools.find_packages(exclude=['docs', 'tests*']),
    classifiers=(
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'requests',
        'marshmallow',
        'pytz'
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"]
)
