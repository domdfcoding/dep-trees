# https://safedep.io/megalodon-mass-github-repo-backdooring-ci-workflows/#full-list-of-compromised-github-repositories

# stdlib
import csv

# 3rd party
from domdf_python_tools.paths import PathPlus

with open("megalodon-campaign-commits.csv", encoding="UTF-8") as fp:
	for row in csv.DictReader(fp):
		full_name = row["repo"]
		username, repo_name = full_name.split('/', 1)

		for filename in PathPlus("output").iterchildren(match="**/*.txt"):
			for line in filename.read_lines():
				if repo_name.lower() in line.lower():
					print(filename, full_name)
