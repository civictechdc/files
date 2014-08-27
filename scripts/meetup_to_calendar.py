import requests, os, json

path = os.path.dirname(os.path.realpath(__file__))

# Set the groups we'd like to grab
groups = ["Code-for-DC","DCLegalHackers","DC-Hack-and-Tell","DC-Web-API-User-Group","Data-Science-DC","Transportation-Techies"]

# Load MEETUP_API_KEY from creds.py
exec(compile(open(path + "/creds.py").read(), path + "/creds.py", 'exec'))

output = []

#Loop through the groups
for g in groups:
    r = requests.get("http://api.meetup.com/2/events?status=upcoming&order=time&limited_events=False&group_urlname="+g+"&desc=false&offset=0&photo-host=public&format=json&page=20&fields=&key="+MEETUP_API_KEY+"&sign=true").json()
    for e in r["results"]:
        output.append(e)

# Save the file as JSON and JSONP
output = json.dumps(output, sort_keys=True, indent=4)

with open(path + '/../calendar.json', 'w') as f:
    f.write(output)

jsonp = "calendar(" + output + ")"

with open(path + '/../calendar.js', 'w') as f:
    f.write(jsonp)
