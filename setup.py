from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in novacept_email_post/__init__.py
from novacept_email_post import __version__ as version

setup(
	name="novacept_email_post",
	version=version,
	description="Email posting for novacept",
	author="Novacept Limited",
	author_email="info@novacept.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
