import csv
import json
from collections import defaultdict

names = {}

givens = defaultdict(int)
titles = defaultdict(int)
allegiances = defaultdict(int)

known_titles = ['Ass Kicker', 'Mischief Maker', 'Chaos Agent', 'Impaler', 'Shark']

def parse(name):
	given_name = ''
	title = ''
	allegiance = ''

	if len(name.split()) < 3:
		given_name = name

	else:
		preposition = 0

		for word in ['of', 'for', 'in']:
			if ' ' + word + ' ' in name:
				preposition = name.split().index(word)

		allegiance = ' '.join(name.split()[preposition + 1:])
		prefix = name.split()[:preposition]

		if len(prefix) == 2:
			given_name = prefix[0]
			title = prefix[1]

		elif prefix:
			if len(prefix) == 3:
				if ' '.join(prefix[1:]) in known_titles:
					given_name = prefix[0]
					title = ' '.join(prefix[1:])
				else:
					given_name = ' '.join(prefix[:2])
					title = prefix[2]

			else:
				if prefix[0] in known_titles:
					title = prefix[0]
				else:
					given_name = prefix[0]

	return given_name, title, allegiance


with open('warriors.csv') as csvfile:
		for row in csv.DictReader(csvfile):
			name = row['name']
			token_id = row['token_id']

			names[token_id] = name
			given_name, title, allegiance = parse(name)

			givens[given_name] += 1
			titles[title] += 1
			allegiances[allegiance] += 1


mapping = {
	0: 'Given Name',
	1: 'Title',
	2: 'Allegiance? Origin?'
}

final = {}

for i, thing in enumerate([givens, titles, allegiances]):
	sorted_tuples = sorted(thing.items(), key=lambda item: item[1])
	final[mapping[i]] = {k: v for k, v in sorted_tuples}


with open('stats.json', 'w') as f:
	json.dump(final, f)

with open('warriors.json', 'w') as f:
    json.dump(names, f)