#!/usr/bin/env python3
#
#  __init__.py
"""
Dependency trees for my projects.
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
from typing import Iterable, Iterator, Tuple

# 3rd party
from domdf_python_tools.iterative import make_tree
from github3 import GitHub
from github3_utils import iter_repos
from packaging.requirements import InvalidRequirement
from pypi_json import PyPIJSON
from shippinglabel.requirements import ComparableRequirement
from tqdm import tqdm

# this package
from dep_trees.utils import get_dependency_tree

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2026 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["make_dep_trees"]


def make_dep_trees(
		github_client: GitHub,
		github_users: Iterable[str] = (),
		github_orgs: Iterable[str] = (),
		pypi_users: Iterable[str] = (),
		) -> Iterator[Tuple[str, str, str]]:
	"""
	Create dependency trees for the given users' and organisations' repositories.

	:param github_client:
	:param github_users:
	:param github_orgs:
	:param pypi_users:

	:returns: An iterator of ``(<repo_name>, <pypi_name>, <tree>)`` tuples.
	"""

	pypi_users = list(pypi_users)

	progbar = tqdm(list(iter_repos(github_client, github_users, github_orgs)))
	for repo in progbar:
		progbar.set_postfix_str(f"{repo.full_name}".ljust(40))

		with PyPIJSON() as pypi:
			try:
				pypi_metadata = pypi.get_metadata(repo.name)
			except InvalidRequirement:
				continue  # TODO: get deps from GitHub in this case (requirements.txt or pyproject.toml)

		if not pypi_metadata.ownership:
			continue  # TODO: get deps from GitHub in this case (requirements.txt or pyproject.toml)

		role_users = {role["user"] for role in pypi_metadata.ownership["roles"]}
		if pypi_users and not any(user in role_users for user in pypi_users):
			continue

		# progbar.set_description(f"{repo.full_name} ({pypi_metadata.name})")

		tree = list(get_dependency_tree(ComparableRequirement(pypi_metadata.name)))

		tree_str = '\n'.join([pypi_metadata.name] + list(make_tree(tree)))
		yield repo.full_name, pypi_metadata.name, tree_str
