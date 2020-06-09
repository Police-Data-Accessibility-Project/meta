# Table of Contents

* [Welcome!](#welcome)
* [Contributing to Scrapers](#contributing-to-scrapers)
	* [General Guidelines](#general-guidelines)
	* [Minimum Requirements for Submission](#minimum-requirements-for-submission)
    * [Testing and Validation](#testing-and-validation)
    * [Getting Help](#getting-help)

# Welcome!

Welcome, and thank you for your interest in contributing to the Police Data Accessibility Project!

There are a number of ways you can help contribute to the project. We need assistance with areas such as Scraper Development, Legal, DevOps, FOIA Requests, and Data Architecture. If you are interested in getting involved with the project beyond Scraper Development (which is the focus of this contribution guideline), please [click here to join our Slack channel](https://join.slack.com/t/policeaccessibility/shared_invite/zt-ego0gttu-MFCPQ6m9aIKiHhOqTRywMQ).

NOTE: We are on a free Slack instance, and the link expires every three weeks. If you attempt to join and the link is invalid, please open an issue and someone will have a new link up shortly. 

# Contributing to Scrapers

## General Guidelines

The majority of scraper code for this project is currently being written in Python. While we are open to conversations about other languages, there is a desire to standardize as much as possible for simplicity of administration and consistency. 

Given the nature of this project, there are some extremely important guidelines below that go along with contributing to web scraping. 

1. Your scraper must be anonymizing data that it gathers, removing identifiable information to prevent disclosure of names of arresting officers or cited citizens.
2. Your scraper must NOT blast websites to the point of denying service to other users or causing the site to show degraded performance. It cannot be overstated how important it is to be gentle on websites we are collecting data from. There are potential legal implications with taking down government-hosted websites. Your scraper should not produce more requests to a website than a real human would. Our general guideline is that you should not be making more than one request per second. {I will be seeking extra input on this value before we post this to the GH}
3. Your scraper must comply with the Terms of Service of the website you are scraping. You are expected to read and understand the TOS of websites you are building scrapers for, and understand that our Github admins will also be reviewing the TOS to ensure your scraper does not violate them. 
4. For now, while we are still examining the legality of bypassing Captchas and authentication pages, please do not write scrapers that bypass them either programatically or with captcha solving services. We will have further guidance on this soon, but will not accept code designed to bypass legitimate authentication and spam prevention services. 

## Minimum Requirements for Submission

Before submitting a pull request for websites, please ensure you have reviewed the General Guidelines in the section above. In addition, good git hygeine is encouraged and appreciated - please squash-and-merge commits and have a clearly stated commit message when submitting pull requests (PR's).  Finally, please fill out the following [Questionnaire](https://forms.gle/QhBwwSpqq3pb3igt8) describing what you are scraping.  This will allow other groups to assess what infrastructure and applications must be developed to support the data you are gathering.

The volunteers working this project are not paid, and are typically doing this work in our free time. Please expect some back-and-forth communication when speaking to the individuals reviewing your PR's and be patient and respectful with us. The more work you do to test and validate that your scraper has met the contribution guidelines, the less back-and-forth will be required. Where we cannot guarantee quality of scrapers, we will reject submissions until the quality checks are met.

## Testing and Validation

{This entire section currently assumes that people will be willing and able to help manage testing of scrapers, which will be a heavy volunteering effort. We need to have more discussions about what this will look like.}

You are expected to test your own scrapers to ensure they are meeting all the guidelines outlined here. You should also expect that a repo admin will perform testing and validation that your scraper meets all the applicable guidelines. We will update specific guidance around testing expectations as the project advances. 

## Getting Help

If you're looking to help, and are finding yourself getting stuck, our Slack channel is the best place to start. The #scraping-public-records-for-police-citation-data channel has a number of developers and administrators who can help you solve issues with scraping, and provide general guidance on expectations. Before utilizing the channel, please read the entire CONTRIBUTING.md document to make sure your questions aren't already answered here.

Thanks again, and we look forward to your contributions!
