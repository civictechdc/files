import json, yaml, requests, os, time, operator, jsonschema, subprocess
from jsonschema import validate

path = os.path.dirname(os.path.realpath(__file__))

# Load credentials for Github
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

# Load in the projects we're tracking
tracked = json.loads(open(path + '/../tracked.json').read())
tracked = tracked["projects"]

output = []

# Load civic.json schema from Code for DC site
schema = requests.get("http://codefordc.org/resources/schema.json").json()

# Begin building
for project in tracked:
    for key, value in project.items():
        name = key
        link = value

    # Get the basic Github data
    url = link.replace('github.com','api.github.com/repos')
    headers = {'Authorization': 'token '+GITHUB_TOKEN}
    r = requests.get(url, headers = headers).json()
    data = {
        'id': r['id'],
        'name': r['name'],
        'description': r['description'],
        'homepage': r['homepage'],
        'html_url': r['html_url'],
        'main_language': r['language'],
        'watchers': r['watchers'],
        'forks': r['forks'],
        'size': r['size'],
        'open_issues': r['open_issues'],
        'created_at': r['created_at'],
        'updated_at': r['updated_at'],
        'pushed_at': r['pushed_at'],
        'default_branch': r['default_branch'],
        'owner': {
            'name': r['owner']['login'],
            'avatar': r['owner']['avatar_url'],
            'url': r['owner']['html_url'],
            'type': r['owner']['type']
        }
    }

    if data['homepage']:
        p = subprocess.Popen(['pa11y','-r','json',data['homepage']], stdout=subprocess.PIPE)
        out, err = p.communicate()
        try:
            out = json.loads(out)
            data["accessibility"] = out["count"]
        except ValueError:
            continue


    # Add in contributor information from Github
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
    data['contributors_count'] = len(contributors)

    # Get Github activity on the default branch for the past year
    activity = requests.get(url+"/stats/participation", headers = headers).json()
    try:
        data['activity'] = activity['all']
    except KeyError:
        time.sleep(4)
        activity = requests.get(url+"/stats/participation", headers = headers).json()
        data['activity'] = activity['all']

    # Get languages used in the Github repo
    languages = requests.get(url+"/languages", headers = headers).json()
    data['languages'] = sorted(languages.iteritems(), key=operator.itemgetter(1), reverse=True)

    # Look for issues tagged as "help wanted"
    issues = requests.get(url+"/issues", headers = headers).json()
    help_wanted = []
    for i in issues:
        for l in i['labels']:
            if l['name'] == 'help wanted':
                issue = {
                    'project': name,
                    'project_url': link,
                    'issue': i['title'],
                    'issue_url': i['html_url'],
                    'body': i['body'],
                    'created_at': i['created_at'],
                    'updated_at': i['updated_at'],
                    'comments': i['comments'],
                    'assignee': i['assignee'],
                    'labels': i['labels']
                }
                help_wanted.append(issue)
    data['help_wanted'] = help_wanted

    # Check if civic.json file is in repo
    # If so, validate it before adding the data
    try:
        civic = requests.get(link.replace('github.com','raw.githubusercontent.com') + '/' + data['default_branch'] + '/civic.json').json()
        try:
            validate(civic,schema)
        except jsonschema.exceptions.ValidationError, error:
            #print error
            print data['name']
            print "\n"
            civic = None
    except ValueError:
        civic = None
    data['civic_json'] = civic

    # Oh yeah, the project's name
    data['name'] = name
    output.append(data)

# Write the JSON, JSONP, and YAML files

json = json.dumps(output, sort_keys=True, indent=4)

with open(path + '/../projects.json', 'w') as f:
    f.write(json)

jsonp = "projects(" + json + ")"

with open(path + '/../projects.js', 'w') as f:
    f.write(jsonp)

yml = yaml.safe_dump(output)

with open(path + '/../projects.yaml', 'w') as f:
    f.write(yml)
