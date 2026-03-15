#!/usr/bin/env python3
#
#  utils.py
"""
Utility functions.
"""
#
#  Copyright © 2026 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from typing import Dict, Iterator, Set

# 3rd party
from domdf_python_tools.iterative import Branch
from github3 import GitHub
from github3.repos import ShortRepository
from github3_utils import iter_repos
from pypi_json import PyPIJSON
from remote_wheel import RemoteWheelDistribution
from shippinglabel.requirements import ComparableRequirement
from shippinglabel_pypi import get_wheel_url

__all__ = ["get_dependencies", "get_dependency_tree", "iter_my_repos"]

dependency_cache: Dict[str, Set[ComparableRequirement]] = {}

users = [
		"domdfcoding",
		]

organizations = [
		"sphinx-toolbox",
		"GunShotMatch",
		"potbanksoftware",
		"python-coincidence",
		"python-formate",
		"repo-helper",
		"PyMassSpec",
		]


def iter_my_repos(client: GitHub) -> Iterator[ShortRepository]:
	"""
	Iterate over repos in my user and organisations.

	:param client:
	"""

	yield from iter_repos(client, users, organizations)


def get_dependencies(requirement: ComparableRequirement) -> Set[ComparableRequirement]:
	"""
	Returns the direct dependencies of the given requirement.

	:param requirement:
	"""

	if requirement.name in dependency_cache:
		return dependency_cache[requirement.name]

	with PyPIJSON() as pypi:
		pypi_metadata = pypi.get_metadata(requirement.name)

	dependencies = set()

	try:
		wheel_url = get_wheel_url(pypi_metadata.name, pypi_metadata.version, strict=True)
	except ValueError:
		# TODO: Try older version or use sdist
		pass
	else:
		with RemoteWheelDistribution.from_url(wheel_url) as wheel:
			for dep in wheel.get_metadata().get_all("Requires-Dist", default=[]):
				if "extra == " in dep:
					continue

				# TODO: check extra against requirement

				dependencies.add(ComparableRequirement(dep))

	dependency_cache[requirement.name] = dependencies

	return dependencies


def get_dependency_tree(requirement: ComparableRequirement) -> Iterator[Branch]:
	"""
	Returns the dependency tree for the given requirement.

	:param requirement:
	"""

	for dep in get_dependencies(requirement):
		if dep.name == requirement.name:
			continue

		# yield dep, list(get_dependency_tree(dep))
		yield str(dep)
		yield list(get_dependency_tree(dep))
