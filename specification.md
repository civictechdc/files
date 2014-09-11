# `civic.json` schema

Our schema is based on the work done by [BetaNYC](https://github.com/BetaNYC/civic.json/blob/master/specification.md).

## File Location and contents
1. `civic.json` shall reside in the root directory of a project's github repository.
2. `civic.json` shall include a single object represented as JSON, with the key/value pairs outlined below.

## Key/Value Specification
1. `status` - text indicating the status of the project.  Any text is allowed, but a selection from the recommended values is advised:

   * `"Ideation"` - Brainstorming phase
   * `"Alpha"` - Brainstorming phase
   * `"Beta"` - Brainstorming phase
   * `"Production"` - Finished Product, development ongoing
   * `"Archival"` - Finished Product, development ongoing


2. `thumbnailUrl` - a URL to an image associated with the project listing.

3. `bornAt` - text indicating the name of the event the project was conceived at, if any.  Any text is allowed.

4. `geography` - text indicating the city, state, county, or other geographic entity this project is relevant to.  Any text is allowed.

        examples: "Washington, DC", "NYC", "Greater Baltimore"

5. `politicalEntity` - a dictionary indicating any political entity to which the project is relevant. The key is the entity's name, and the value is the entity's URL.

        example: {"DC Council": "http://www.dccouncil.washington.dc.us/"}

6.  `governmentPartner` - a dictionary indicating any political entity with which the project is working. The key is the entity's name, and the value is the entity's URL.

        example: {"DC Council": "http://www.dccouncil.washington.dc.us/"}

7.  `communityPartner` - a dictionary indicating the community organizations with which the project is working. The key is the org's name, and the value is the org's URL.

        example: {"Bread for the City": "http://www.breadforthecity.org/"}

8. `type` - text describing the type of project.  Any text is allowed, but a selection from the recommended values is advised:

   * `"Web App"`
   * `"Mobile App"`
   * `"Policy Document"`
   * `"Dataset"`


9. `needs` - an array of "need" or "want" objects.  Needs are considered necessary to the success of the project, while wants are considered enhancements.  There is no limit to the number of objects included in a project.

10. `need` or `want` - text indicating a need or want of the project.  This can be a skillset that is needed, or any other resource.  Any text is allowed.

        examples: "Web Designer", "Web Hosting", "Political Sponsorship"

11. `categories` - an array of "category" objects.  There is no limit to the number of categories included in a project.

12. `category` - text indicating the category of the project.  Any text is allowed.

        examples:  "Land Use", "Transportation", "Politics", "Financial", "Open Data"

13. `moreInfo` - a URL to a document or site with more information about the project, such as a Hackpad or Google Doc.

## Example civic.json

```
{
    "status": "Production",
    "thumbnailUrl":"http://ancfinder.org/static/img/favicon.png",
    "needs": [
        {"need":"ANC document uploading"},
        {"need":"Python"}
    ],
    "bornAt": "Code for DC",
    "type": "Web App",
    "categories": [
        {"category":"Politics"},
        {"category":"Government"},
        {"category":"Open Data"}
    ],
    "geography": "Washington, DC",
    "contact":
        {
            "name": "",
            "email": "contactus@ancfinder.org",
            "twitter": "@ancfinder"
        },
    "communityPartner": {},
    "politicalEntity": {"Office of Advisory Neighborhood Commissions":"http://anc.dc.gov/"},
    "governmentPartner": {},
    "moreInfo": ""
}
```
