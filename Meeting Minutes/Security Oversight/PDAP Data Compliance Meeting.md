# PDAP Data Compliance Meeting

- Alex Shkolnik - data security data compliance expert at McKinsey

- Two primary risks
	- scraping
		- Biggest piece of advice is “have you exhausted every single option?” There are much more simple ways - scraping is extremely complex
		- If scraping is the only option, don’t hide from a site that you’re scraping (no proxies), generally, the terms of use are not enforceable but a pay wall is obviously not something to try to bypass (captchas, paywall, rate limiters, etc.), don’t cause denial of service inadvertently, be cautious about copyright or patented data, 
	- handling PII
		- Can we “re-home” public data which includes PII?
			- Certainly not as troublesome as possible - just note where it came from. If we sold it it would be a much different issue

- Have a good sense of use cases
	- The traditional is getting every you can and then figure it out later (we don’t want to do this)
	- Current guidance is tailored, focus on going after what you want and ignore the other stuff
		- Side note, Jeremy talked about having researches develop questions so this can be more codified as to what is actually needed

- Don’t dos
	- don’t taint the data set with ToS violations, etc.

Privacy
- Key to good privacy is why collecting it, what it’s used for, be specific, know every reason why in case someone asks
- Try to de-risk the data - encrypting, hashing, shortening it, etc. (e.g. do I need the whole ZIP code? or just the city? Do I truly need the names of the arrested individuals - does it really matter? Or just the circumstances?)
- Security issues start when data is stored in disparate places (including multiple servers, device, etc.) - centralize all the data and put it in it’s final resting place (more places it’s been, more prone to failure of integrity)
- Anonymous data - more conceptual than reality, data is “pseudonymized” but not completely (anonymized means no way to identify individual - very high bar of success - may actually be hypothetical)
- More practically, be very cautious about children’s data (children under 16). The US has silo’s of industry of children’s data that are governed by law
- Sensitive data - DL’s, Passports, License Numbers, SSN - just keep it out. Race and religion are protected data as well

- Main takeaways
	- Investigate all alternatives of gathering data legally before scraping
	- Be extremely transparent with sites you scrape from - do not use proxies or anonymizers
	- Filter out the PII, etc. during collection not after
	- Annotate the data as to where it came from, what it’s used for, what questions we intend to answer from it, etc.
	- Don’t have to worry about compliance regulations (except for maybe CCPA) - needs to be investigated further (work with legal resource)
	- Try to de-risk the data as much as possible
	- Be cautious about children’s data (children under 16) and race and religion


