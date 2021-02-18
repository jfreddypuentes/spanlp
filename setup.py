import setuptools as st

with open('README.md', 'r') as readme_file:
    _long_description = readme_file.read()

st.setup(
    name='spanlp',
    packages=st.find_packages(include=['spanlp', 'spanlp.*']),
    version='1.0.1',
    description='A fast, robust Python library to check for profanity or offensive language in Spanish strings.'
                'It contains all the rude words of Spanish-speaking countries (Argentina, Bolivia, Chile, Colombia, '
                'Costa Rica, Cuba, Ecuador, El Salvador, España, Guatemala, Guinea Ecuatorial, Honduras, Mexico, '
                'Nicaragua, Panama, Paraguay, Peru, Puerto Rico, Dominicana, Uruguay, Venezuela)',
    long_description=_long_description,
    long_description_content_type="text/markdown",
    author='Jhon Freddy Puentes',
    author_email='jfredypuentes@gmail.com',
    license='MIT',
    url="https://github.com/jfreddypuentes/spanlp",
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==6.1.2'],
    test_suite='tests',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Development Status :: 5 - Production/Stable',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Operating System :: OS Independent",
    ],
    data_files=[('data', [
        'spanlp/dataset/ARG.txt',
        'spanlp/dataset/BOL.txt',
        'spanlp/dataset/CHL.txt',
        'spanlp/dataset/COL.txt',
        'spanlp/dataset/CRI.txt',
        'spanlp/dataset/CUB.txt',
        'spanlp/dataset/ECU.txt',
        'spanlp/dataset/SLV.txt',
        'spanlp/dataset/ESP.txt',
        'spanlp/dataset/GTM.txt',
        'spanlp/dataset/GNQ.txt',
        'spanlp/dataset/HND.txt',
        'spanlp/dataset/MEX.txt',
        'spanlp/dataset/NIC.txt',
        'spanlp/dataset/PAN.txt',
        'spanlp/dataset/PRY.txt',
        'spanlp/dataset/PER.txt',
        'spanlp/dataset/PRI.txt',
        'spanlp/dataset/DOM.txt',
        'spanlp/dataset/URY.txt',
        'spanlp/dataset/VEN.txt'
    ]),],
    package_data={
        '': ['spanlp/dataset/*'],
    },
    include_package_data=True,
    python_requires='>=3.6',
)
