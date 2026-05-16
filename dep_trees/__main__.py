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
from domdf_python_tools.paths import PathPlus
from github3 import GitHub

# this package
from dep_trees import make_dep_trees

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

gh = GitHub(token=os.environ["GITHUB_TOKEN"])

output_dir = PathPlus("output")
output_dir.maybe_make()

# TODO: config file to allow users and orgs to be specified
for repo_name, pypi_name, tree in make_dep_trees(gh, users, organizations, {"DomDF"}):

	# print(get_dependencies(pypi_name))
	# for dep in get_dependencies(pypi_name):
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

	# print(pypi_name)
	# print("\n".join(make_tree(tree)))

	output_dir.joinpath(pypi_name).write_clean(tree)
