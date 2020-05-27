# Police Data Accessibility Project

Rough Mission Statement (will evolve):

It is my belief that perhaps the single most effective way we can make concrete progress toward this goal is in the realm of data accessibility. Specifically the accessibility of granular, local, county level police citation data.

This however, is a big undertaking, as most counties have clumsy/antiquated systems for searching for and extracting this type of data, and almost none have fully exposed datasets.

Ultimately, the future goal for this initiative is to:

Request (via FOIA) or Scrape, and then clean and aggregate county level police citation data for as many counties as possible, and to most importantly make this data open and free to the public.
I believe doing so will enable citizen data scientists and data journalists to then make progress on analysis, whereby they will serve the public by looking for and finding trends and anomalies in police behavior, leading to more accountability for both individual police officers and their larger police organizations.




Initial Goals:

Scraping:

1. Many counties outsource their court records data to third parties. Tyler Technologies is one such vendor. They make the court records portals for what seems like at least a few dozen counties. Finding and building scrapers for portals that are the same for many counties seems like a great early goal. 

2. Finding and writing scrapers for other large counties. Prioritize counties with easier to scrape systems first. 


Freedom of Information Act Requests:

3. Researching a data request template with all the data we want to ask for in FOIA requests

4. Submitting FOIA requests and monitoring responses


I will be adding tasks to the projects section of this repo, so we can all keep track of them there.


If you are looking to start building a scraper, the csv file above has the URLS of all most US counties' public records portals. 

The fields we would like to make sure to collect at a minimum from any scrape are:

_id
_state
_county
CaseNum
FirstName
MiddleName
LastName
Suffix
DOB
Race
Sex
ArrestDate
FilingDate
OffenseDate
DivisionName
CaseStatus
DefenseAttorney
PublicDefender
Judge
ChargeCount
ChargeStatute
ChargeDescription
ChargeDisposition
ChargeDispositionDate
ChargeOffenseDate
ChargeCitationNum
ChargePlea
ChargePleaDate
ArrestingOfficer
ArrestingOfficerBadgeNumber

