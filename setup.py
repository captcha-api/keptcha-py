from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

short_description = (
    "keptcha is an API wrapper for https://captcha-api.akshit.me written in Python."
)
long_description = (here / "README.md").read_text(encoding="utf-8")

github_url = "https://github.com/captcha-api/keptcha-py"

setup(
    name="keptcha",
    version="0.1.2",
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=github_url,
    author="Syed_Ahkam",
    author_email="smahkam313@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="captcha, api, wrapper, async",
    packages=find_packages(),
    python_requires=">=3.6",
    project_urls={"Website": "https://captcha-api.akshit.me", "Source": github_url},
)
