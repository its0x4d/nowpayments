import setuptools

requirements = [
    "requests==2.28.1"
]

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name="nowpayment",
    version="1.6.1",
    author="Mostafa Mosavi",
    author_email="mostafa.uwsgi@gmail.com",
    description="A NowPayments.io client for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/its0x4d/nowpayments",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires='>=3.6',
)
