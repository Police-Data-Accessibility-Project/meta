# Contributing to PDAP

Welcome, and thank you for your interest in contributing to the Police Data Accessibility Project!

There are a number of ways you can help contribute to the project, including code. 

# Contributing to Scrapers

## General Guidelines

The majority of scraper code for this project is written in Python. We're open to other languages, but please be prepared to document your work.

Your scraper must follow these [legal guidelines](https://docs.google.com/document/d/1gjnH0S18iBI20K1pfs4M3wuMqcLE_ZSgt71ITUY2Fbk/edit).

Everyone working on this project is using their free time. Please expect some back-and-forth communication when speaking to the individuals reviewing your PR's and be patient and respectful with us. The more work you do to test and validate that your scraper has met the contribution guidelines.

## Minimum Requirements for Submission

1. Before submitting a pull request (PR) review the General Guidelines above.
2. Good git hygeine is encouraged and appreciated: squash-and-merge commits and have a clearly stated commit message when submitting PRs.
3. Fill out the following [Questionnaire](https://forms.gle/QhBwwSpqq3pb3igt8) describing what you are scraping.

## Getting Help

If you're looking to help, and are finding yourself getting stuck, our Slack channel is the best place to start. The #scraping-public-records-for-police-citation-data channel has a number of developers and administrators who can help you solve issues with scraping, and provide general guidance on expectations. Before utilizing the channel, please read the entire CONTRIBUTING.md document to make sure your questions aren't already answered here.

Thanks again, and we look forward to your contributions!

## Scraping specifics

1. Many counties outsource their court records data to third party vendors such as Tyler Technologies. Finding and building scrapers for portals that are the same for many counties is a potential early goal. A list of counties court record systems and their vendors must be made. This will be done collaboratively in [this Google Sheet](https://docs.google.com/spreadsheets/d/1nD4LnjU1b1b9RgQNcn6op-Oj3ZQVcgz-2bUgEU5RVXA/edit). For more details see https://github.com/Police-Data-Accessibility-Project/Police-Data-Accessibility-Project/issues/6.

For guidelines to contributing to scraping, please see [CONTRIBUTING.md](CONTRIBUTING.md)

### Known datasets

This [dataset catalogue](https://drive.google.com/drive/folders/1G4L1PgaexT1B78So5MoS95hIwcB4DbAR?usp=sharing) is how we track potential sources.

### Fields to scrape

* _id
* _state
* _county
* CaseNum
* FirstName
* MiddleName
* LastName
* Suffix
* DOB
* Race
* Sex
* ArrestDate
* FilingDate
* OffenseDate
* DivisionName
* CaseStatus
* DefenseAttorney
* PublicDefender
* Judge
* ChargeCount
* ChargeStatute
* ChargeDescription
* ChargeDisposition
* ChargeDispositionDate
* ChargeOffenseDate
* ChargeCitationNum
* ChargePlea
* ChargePleaDate
* ArrestingOfficer
* ArrestingOfficerBadgeNumber.
