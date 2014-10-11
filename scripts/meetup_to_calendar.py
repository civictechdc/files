import requests, os, json, yaml, operator

path = os.path.dirname(os.path.realpath(__file__))

# Load the groups we'd like to grab
tracked = json.loads(open(path + '/../tracked.json').read())
tracked = tracked["meetups"]

# Load MEETUP_API_KEY from creds.py
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

output = {}
output["codefordc"] = []
output["other"] = []

# Get Code for DC events
r = requests.get("http://api.meetup.com/2/events?status=upcoming&order=time&limited_events=False&group_urlname=Code-for-DC&desc=false&offset=0&photo-host=public&format=json&page=20&fields=&key="+MEETUP_API_KEY+"&sign=true").json()
for e in r["results"]:
    output["codefordc"].append(e)

# Loop through the other groups
for g in tracked:
    r = requests.get("http://api.meetup.com/2/events?status=upcoming&order=time&limited_events=False&group_urlname="+g+"&desc=false&offset=0&photo-host=public&format=json&page=20&fields=&key="+MEETUP_API_KEY+"&sign=true").json()
    for e in r["results"]:
        output["other"].append(e)

# Sort events by date
output["other"] = sorted(output["other"], key=operator.itemgetter('time'))

# Write the JSON, JSONP, and YAML files

json = json.dumps(output, sort_keys=True, indent=4)

with open(path + '/../calendar.json', 'w') as f:
    f.write(json)

jsonp = "calendar(" + json + ")"

with open(path + '/../calendar.js', 'w') as f:
    f.write(jsonp)

yml = yaml.safe_dump(output)

with open(path + '/../calendar.yaml', 'w') as f:
    f.write(yml)
