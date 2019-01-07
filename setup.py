
import setuptools

setuptools.setup(
    name='weekplot',
    version='0.1.0',
    include_package_data=True,
    packages=[
        'weekplot',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
        'matplotlib>=3.0.0,<4.0.0',
        'PyYAML>=3.13,<4.0'
    ],
    entry_points={
        'console_scripts': ['weekplot=weekplot:main'],
    }
)
