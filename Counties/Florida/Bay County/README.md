# Florida: Bay County

Bay County uses a Benchmark portal by Pioneer Technology .

* There is a very simple addition captcha.
* Search parameters are limited, there are no filters for date/time. 
* No search can give more than 5000 results, meaning searches will need to be specific enough to restrict cases below 5000.


## Installation

### Local installation

1. Install Python 3.8

2. `cd Scraper`

3. `pip install -r requirements.txt`

4. Install [Firefox](https://www.mozilla.org/en-US/firefox/new/)

5. Install [Gecko webdriver](https://github.com/mozilla/geckodriver/releases)

6. Verify the webdriver is installed in PATH by entering `geckodriver --help` in CMD.

7. Install [Tesseract](https://tesseract-ocr.github.io/tessdoc/Home.html)

8. Verify tesseract is installed in PATH by opening cmd and entering `tesseract`.

9. `python3 Scraper.py [args]` (See below for args) 

### Dockerized installation

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)

2. `cd Scraper`

3. `docker-compose build scraper`

4. `docker-compose run scraper bash`

5. `python3 Scraper.py [args]` (See below for args)

## Args

|Short|Long|Default Value|Description|
|---|---|---|---|
|`-p`|`--portal-base`|https://court.baycoclerk.com/BenchmarkWeb2/|Base URL for the Benchmark-based portal|
|`-s`|`--state`|FL|Postal code for state being scraped.
|`-c`|`--county`|Bay|County being scraped.
|`-y`|`--start-year`|2000|Earliest year to scrape as 4-digit year.|
|`-e`|`--end-year`|2020|Latest year to scrape as 4-digit year.|
|`-t`|`--missing-thresh`|5|How many missing cases in a row to allow before proceeding to the next year.|
|`-p`|`--collect-pii`|N/A (Off by default)|Collect Personally Identifiable Information (PII).|
|`-c`|`--connect-thresh`|10|How many times to attempt to connect to a page before failing.
|`-o`|`--output`|bay-county-scraped|Output CSV name. The .csv file extension is not required.
|`-a`|`--save-attachments`|none|Save case docket attached documents. Disabled by default as these documents contain embedded PII. Valid values: `none` / `filing` / `all`. The `filing` option saves only attachments related to the case or citation filing.
|`-u`|`--solve-captchas`|N/A (Off by default)|Automatically solve captchas used on the portal.
|`-v`|`--verbose`|N/A (Off by default)|Run in Verbose mode with lots of printing

### Search Method: Case Number
There are only 3 ways to search for cases. Name, Case Number, and Citation Number. Only Case Number is viable for ensuring a complete dataset.


`The Case Numbers used for searching this portal are not the same as the Uniform Case Numbering System. Store the Portal Case Number in 'PortalID' and the Uniform Case Number in 'CaseNum'.`

The portal's case numbers looks like this: 92000001CFMA. Let's decompose this...

The first two digits **92** signify the year of filing. 1992 in this case. 

The following 6 digits **000001** signify the case number that year. This was the first case filed that year.

The next 2-4 characters signify the court filing type. This does not need to be included in the search.

Cases can be opened iteratively by searching 92000001, 92000002, 92000003, ... until no case is found.

Unfortunately, there are some gaps in the data where a case is missing. I'm unsure for the reason for this, perhaps the case has not concluded, or it was removed.

In this scenario, `missing-threshold` is defined, where after N missing cases, it is assumed all cases for that year have been explored.

### Solving Captcha

Automated captcha solving is disabled by default.

The Captcha is screenshotted with selenium. It is then converted to HSV and thresholded as in [this post](https://stackoverflow.com/a/53978868/6008271). Tesseract is used for OCR.

Correctly solved Captchas are saved to `captcha/correct`. Incorrectly solved Captchas are saved to `captcha/incorrect`.

In the case a Captcha is solved incorrectly, the portal does not present a new Captcha on refresh. 
To get around this, cookies are cleared and then upon refresh a new captcha is presented.

### Collecting Personally Identifiable Information (PII)

By default, the scraper does not collect any PII in compliance with our design guidelines.


### Uniform Case Numbering System

The State of Florida has mandated that court records published on the Internet for general public access be numbered with a Uniform Case Numbering System.

This numbering system's meaning can be found [in this PDF](https://www.flcourts.org/content/download/219191/1981092/AO_Uniform_Case_Numbering_12-03-98_amended.pdf).

### Plea

If a plea was made, this does not show in the 'plea' field but instead written in the Case Dockets. This is annoying as the dockets appear to be human-typed so appear in slightly different formats.

The last digit refers to which charge(s) this applies to, though this is not aways present.
### Defense Attorney

Defense attorneys are also only included in the docket text and can also appear in different formats.

Multiple defense attorneys can be found for a single case.
