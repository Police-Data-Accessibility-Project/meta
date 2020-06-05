# Police Data Accessibility Project

Our mission is to enable a more transparent and empowered society by making law enforcement public records open source and easily accessible to the public. 

> # [Join the Slack](https://join.slack.com/t/policeaccessibility/shared_invite/zt-ego0gttu-MFCPQ6m9aIKiHhOqTRywMQ)

Law enforcement data, especially at the local level, is hidden in the corners of the internet, obfuscated by bureaucracy, and served up via low quality user experiences. All this makes it difficult for citizens to access, consolidate, and make use of the data for accurate and factual inferences. Our approach empowers volunteer hunter-gatherers to contribute to a product empowering the citizenry with oversight capability.

Our product is a consolidated, publicly available library of law enforcement related records. Our goal is to ease data consumption, facilitate open source software analytics, and provide an interface for reporting and analysis of law enforcement activity. Our product will be made publicly available, free of charge.

Our target user demographic is the data analytics and justice sector so they may examine law enforcement trends. The product will also benefit broader swathes of the population, such as academics studies, press coverage, government oversight, elected officials, and the law enforcement agencies themselves.

## Stage of Development

This venture started up in early May 2020 out of an established Slack-GitHub-Discord-Reddit community of contributors, which as of the end of May 2020 numbers 2,000+ volunteers and growing. Our initial research shows similar, splintered online communities and organizations with the mission to provide law enforcement oversight. However, they often do not make their data easily accessible, are focused on a small geographic area, or are simply not up to date. 

Our international volunteer community is actively scraping data from existing sites, publicly available government sites, and making initial Freedom of Information Act (FOIA) requests to gather data via our GitHub published rules of conduct. We have a basic operating structure and wish to scale responsibly and sustainably. Our next major milestone is to establish a nonprofit entity. Our initial research into 501c organizations indicates it is no small task, and we need help to do it well.

## Initial Goals:

Ultimately, the future goal for this initiative is to:

Request (via FOIA) or Scrape, and then clean and aggregate county level police citation data for as many counties as possible, and to most importantly make this data open and free to the public.
I believe doing so will enable citizen data scientists and data journalists to then make progress on analysis, whereby they will serve the public by looking for and finding trends and anomalies in police behavior, leading to more accountability for both individual police officers and their larger police organizations.

### Scraping:

1. Many counties outsource their court records data to third party vendors such as Tyler Technologies. Finding and building scrapers for portals that are the same for many counties seems like a great early goal. A list of counties court record systems and their vendors must be made. This will be done collaboratively in [this Google Sheet](https://docs.google.com/spreadsheets/d/1nD4LnjU1b1b9RgQNcn6op-Oj3ZQVcgz-2bUgEU5RVXA/edit). For more details see https://github.com/Police-Data-Accessibility-Project/Police-Data-Accessibility-Project/issues/6.

1. Finding and writing scrapers for other large counties. Prioritize counties with easier to scrape systems first. 

For guidelines to contributing to scraping, please see [CONTRIBUTING.md](CONTRIBUTING.md)

### Freedom of Information Act Requests:

1. Researching a data request template with all the data we want to ask for in FOIA requests

1. Submitting FOIA requests and monitoring responses


We will be adding tasks to the projects section of this repo, so we can all keep track of them there.


If you are looking to start building a scraper, the csv file above has the URLS of all most US counties' public records portals. 

### The datasets we have already collected or gained access to are:

This [Google Sheet](https://docs.google.com/spreadsheets/d/1yyjYV1BLFuLy32CW66zApuEWDSFrR9Dw9y49MU7dxcQ/edit) will track datasets created by other open projects or that members of PDAP have acquired.

### The fields we would like to make sure to collect at a minimum from any scrape are:

**For anything labeled PII: do not scrape personally identifiable information yet. We are consulting with lawyers on implications for this, but intend to do so once given the green light. 

* _id
* _state
* _county
* CaseNum (**PII**, for now)
* FirstName (**PII**)
* MiddleName (**PII**)
* LastName (**PII**)
* Suffix
* DOB (**PII**)
* Race
* Sex
* ArrestDate
* FilingDate
* OffenseDate
* DivisionName
* CaseStatus
* DefenseAttorney (**PII**)
* PublicDefender (**PII**)
* Judge (**PII**)
* ChargeCount
* ChargeStatute
* ChargeDescription
* ChargeDisposition
* ChargeDispositionDate
* ChargeOffenseDate
* ChargeCitationNum
* ChargePlea
* ChargePleaDate
* ArrestingOfficer (**PII**)
* ArrestingOfficerBadgeNumber.  (**PII**)

