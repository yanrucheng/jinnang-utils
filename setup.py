from setuptools import setup, find_packages

setup(
    name='jinnang-utils',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'':'src'},
    install_requires=[
        # Add your project dependencies here, e.g., 'requests>=2.20.0',
    ],
    python_requires='>=3.6',
    description='A collection of utility functions.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yanrucheng/jinnang-utils',
    author='Cheng Yanru',
    author_email='yanru@cyanru.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)