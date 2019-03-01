import setuptools
import sys

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

version = "0.0.1"

if '-v' in sys.argv:
    index = sys.argv.index('-v')
    sys.argv.pop(index)
    version += '.dev' + sys.argv.pop(index)

setuptools.setup(
    name='annotationfactory',
    version=version,
    description="annotation factory python sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Microsoft/Annotation-Factory",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'jinja2',
        'jsonschema',
        'xmltodict'
    ],
    package_data={
        'annotationfactory': ['templates/*', 'models/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
