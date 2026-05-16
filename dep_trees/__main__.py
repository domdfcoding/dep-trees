#!/usr/bin/env python3
#
#  __main__.py
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
import os

# 3rd party
from domdf_python_tools.iterative import make_tree
from domdf_python_tools.paths import PathPlus
from github3 import GitHub
from packaging.requirements import InvalidRequirement
from pypi_json import PyPIJSON
from shippinglabel.requirements import ComparableRequirement
from tqdm import tqdm

# this package
from dep_trees.utils import get_dependency_tree, iter_my_repos

gh = GitHub(token=os.environ["GITHUB_TOKEN"])

output_dir = PathPlus("output")
output_dir.maybe_make()

for repo in tqdm(list(iter_my_repos(gh))):

	with PyPIJSON() as pypi:
		try:
			pypi_metadata = pypi.get_metadata(repo.name)
		except InvalidRequirement:
			continue

	if not pypi_metadata.ownership:
		continue

	role_users = {role["user"] for role in pypi_metadata.ownership["roles"]}
	if "DomDF" not in role_users:
		continue

	# print(get_dependencies(pypi_metadata.name))
	# for dep in get_dependencies(pypi_metadata.name):
	# 	print(dep)
	# 	for dep_dep in get_dependencies(dep):
	# 		print(" ", dep_dep)
	# 		for dep_dep_dep in get_dependencies(dep_dep):
	# 			print("   ", dep_dep_dep)
	# 			print("     ", get_dependencies(dep_dep_dep))
	# 			for dep_dep_dep_dep in get_dependencies(dep_dep_dep):
	# 				print("     ", dep_dep_dep_dep)
	# 				print("       ", get_dependencies(dep_dep_dep_dep))
	# 				for dep_dep_dep_dep_dep in get_dependencies(dep_dep_dep_dep):
	# 					print("       ", dep_dep_dep_dep_dep)
	# 					print("         ", get_dependencies(dep_dep_dep_dep_dep))

	tree = list(get_dependency_tree(ComparableRequirement(pypi_metadata.name)))

	# print(pypi_metadata.name)
	# print("\n".join(make_tree(tree)))

	output_dir.joinpath(pypi_metadata.name).write_lines([pypi_metadata.name] + list(make_tree(tree)))
