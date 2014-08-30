import json, requests, os, time, operator, validictory

path = os.path.dirname(os.path.realpath(__file__))

# Load
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

# Load in the projects we're tracking
tracked = json.loads(open(path + '/../tracked.json').read())

output = []

# Create schema for JSON validation
schema = {
    "type":"object",
    "properties":{
        "status":{
            "type":"string",
            "blank":True
        },
        "thumbnailUrl":{
            "type":"string",
            "blank":True
        },
        "contact":{
            "type":"object",
            "properties":{
                "name":{
                    "type":"string",
                    "blank":True
                },
                "email":{
                    "type":"string",
                    "blank":True
                },
                "twitter":{
                    "type":"string",
                    "blank":True
                }
            }
        },
        "bornAt":{
            "type":"string"
        },
        "geography":{
            "type":"string",
            "pattern":"^Washington, DC$"
        },
        "politicalEntity":{
            "type":"object"
        },
        "governmentPartner":{
            "type":"object"
        },
        "communityPartner":{
            "type":"object"
        },
        "type":{
            "type":"string",
            "blank":"True"
        },
        "needs":{
            "type":"array"
        },
        "categories":{
            "type":"array"
        },
        "moreInfo":{
            "type":"string",
            "blank":True
        }
    }
}

for project in tracked:
    for key, value in project.items():
        name = key
        link = value
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
    try:
        data['activity'] = activity['all']
    except KeyError:
        time.sleep(4)
        activity = requests.get(url+"/stats/participation", headers = headers).json()
        data['activity'] = activity['all']
    languages = requests.get(url+"/languages", headers = headers).json()
    data['languages'] = sorted(languages.iteritems(), key=operator.itemgetter(1), reverse=True)
    try:
        civic = requests.get(link.replace('github.com','raw.githubusercontent.com') + '/master/civic.json').json()
        try:
            validictory.validate(civic,schema)
        except ValueError, error:
            print error
            print civic
            print "\n\n"
#            civic = None
    except ValueError:
        civic = None
    data['civic_json'] = civic
    data['name'] = name
    output.append(data)

output = json.dumps(output, sort_keys=True, indent=4)

with open(path + '/../projects.json', 'w') as f:
    f.write(output)

jsonp = "projects(" + output + ")"

with open(path + '/../projects.js', 'w') as f:
    f.write(jsonp)
