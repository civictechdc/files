import json, requests, os, time

path = os.path.dirname(os.path.realpath(__file__))

# Load
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

# Load in the projects we're tracking
tracked = json.loads(open(path + '/../tracked.json').read())

output = []

for project in tracked:
    for key, value in project.items():
        name = key
        link = value
    url = link.replace('github.com','api.github.com/repos') + '/issues'
    headers = {'Authorization': 'token '+GITHUB_TOKEN}
    r = requests.get(url, headers = headers).json()
    for i in r:
        for l in i['labels']:
            if l['name'] == 'help wanted':
                output.append({
                    'project': name,
                    'project_url': link,
                    'issue': i['title'],
                    'issue_url': i['html_url'],
                    'body': i['body'],
                    'created_at': i['created_at'],
                    'updated_at': i['updated_at'],
                    'comments': i['comments'],
                    'assignee': i['assignee']
                })

output = json.dumps(output, sort_keys=True, indent=4)

with open(path + '/../help_wanted.json', 'w') as f:
    f.write(output)

jsonp = "help_wanted(" + output + ")"

with open(path + '/../help_wanted.js', 'w') as f:
    f.write(jsonp)
