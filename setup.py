from distutils.core import setup

setup(
    name='Cupcake Lovers Store',
    version='0.1',
    packages=['cupcakestore', 'accounts', 'app','carts','checkout','customer','store'],
    license="MIT License",
    long_description=open('README.txt').read()
)