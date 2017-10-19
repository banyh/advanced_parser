from setuptools import setup, find_packages

reqs = [
    'Pillow',
    'bs4',
    'langdetect',
]

setup(
    name='advanced_parser',
    version='0.1',
    description='an easy-to-scale parser',
    url='https://github.com/banyh/advanced_parser',
    author='Ping Chu Hung',
    author_email='banyhong@gliacloud.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=reqs,
)
