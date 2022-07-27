import os
import setuptools

def requirements():
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt"), encoding="utf-8") as f:
        return f.read().splitlines()

setuptools.setup(
    name="Default Scrapper",
    version="1.0.0",
    license="MIT",
    author="Seongbum Seo",
    author_email="sbumseo@bigpicture.team",
    description="Web Scrapper",
    long_description=open("README.md").read(),
    url="https://github.com/bigpicture-kr/default-scrapper",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=requirements(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
)