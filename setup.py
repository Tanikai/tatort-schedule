import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tatort-schedule",
    version="0.1.0",
    author="Tanikai",
    author_email="kai.anter@web.de",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tanikai/tatort-schedule",
    project_urls={
        "Bug Tracker": "https://github.com/Tanikai/tatort-schedule/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
    install_requires=[
        "beautifulsoup4",
        "python-dateutil"
    ]
)