import json, requests, os

path = os.path.dirname(os.path.realpath(__file__))

file_name = path + '/../projects.json'

file = json.loads(open(file_name).read())
projects = file['tracked']

file['projects'] = {}

for p in projects:
    for key, value in p.items():
        name = key
        link = value
    q = link.replace('github.com','api.github.com/repos')
    r = requests.get(q).json()
    data = {
        'id': r['id'],
        'name': r['name'],
        'description': r['description'],
        'homepage': r['homepage'],
        'html_url': r['html_url'],
        'language': r['language'],
        'watchers_count': r['watchers_count'],
        'contributors_url': r['contributors_url'],
        'forks_count': r['forks_count'],
        'open_issues': r['open_issues'],
        'created_at': r['created_at'],
        'updated_at': r['updated_at'],
        'pushed_at': r['pushed_at'],
        'owner': {
            'name': r['owner']['login'],
            'avatar': r['owner']['avatar_url'],
            'url': r['owner']['html_url'],
            'type': r['owner']['type']
        }
    }
    try:
        c = requests.get(link.replace('github.com','raw.githubusercontent.com') + '/master/civic.json').json()
    except ValueError:
        c = None
    data['civic_json'] = c
    file['projects'][name] = data

output = json.dumps(file, sort_keys=True, indent=4)

with open(file_name, 'w') as f:
    f.write(output)
