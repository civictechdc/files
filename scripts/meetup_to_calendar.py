import requests, os, json, yaml

path = os.path.dirname(os.path.realpath(__file__))

# Load the groups we'd like to grab
tracked = json.loads(open(path + '/../tracked.json').read())
tracked = tracked["meetups"]

# Load MEETUP_API_KEY from creds.py
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

output = []

#Loop through the groups
for g in tracked:
    print g
    r = requests.get("http://api.meetup.com/2/events?status=upcoming&order=time&limited_events=False&group_urlname="+g+"&desc=false&offset=0&photo-host=public&format=json&page=20&fields=&key="+MEETUP_API_KEY+"&sign=true").json()
    for e in r["results"]:
        output.append(e)

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
