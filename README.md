Files
=====

These files are used in other Code for DC projects, but needed a place to live. Here's what they are:

`civic.json.template`: a template for the `civic.json` files used to power Code for DC's projects page.

`specification.md`: an explanation of how the `civic.json` file works.

`projects.json`: the data about our projects to power `projects.html` on [codefordc.org]().

`tracked.json`: the names and repo addresses of all of our projects.

`calendar.json`: meeting information for Code for DC and various other local groups.

## Running things

Currently, this repo is updated as a cron job with the following shell script:

```
#! /bin/sh

cd /path/to/repo
git pull
python scripts/civic_json.py
python scripts/meetup_to_calendar.py
git add .
git commit --allow-empty -m "auto-update for $(date +'%F at %R')"
git push origin master
```
