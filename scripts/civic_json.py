import json, requests, os

path = os.path.dirname(os.path.realpath(__file__))

file_name = path + '/../projects.json'
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

file = json.loads(open(file_name).read())
tracked = file['tracked']

file['projects'] = []

for project in tracked:
    for key, value in project.items():
        name = key
        link = value
    url = link.replace('github.com','api.github.com/repos')
    headers = {'Authorization': 'token 3f446009ac6bab1385940a7808f6edd22a0e49c4'}
    r = requests.get(url, headers = headers).json()
    data = {
        'id': r['id'],
        'name': r['name'],
        'description': r['description'],
        'homepage': r['homepage'],
        'html_url': r['html_url'],
        'language': r['language'],
        'watchers_count': r['watchers_count'],
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
    contributors = []
    con = requests.get(r['contributors_url'], headers = headers).json()
    for c in con:
        contributors.append({
            'name': c['login'],
            'avatar_url': c['avatar_url'],
            'link': c['html_url'],
            'contributions': c['contributions']
        })
    data['contributors'] = contributors
    activity = requests.get(url+"/stats/participation", headers = headers).json()
    data['activity'] = activity['all']
    try:
        civic = requests.get(link.replace('github.com','raw.githubusercontent.com') + '/master/civic.json').json()
    except ValueError:
        civic = None
    data['civic_json'] = civic
    data['name'] = name
    file['projects'].append(data)

output = json.dumps(file, sort_keys=True, indent=4)

with open(file_name, 'w') as f:
    f.write(output)
