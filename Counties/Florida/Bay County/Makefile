init:
	pip3 install -r ./Scraper/requirements.txt
scrape: init
	python3 ./Scraper/Scraper.py
test: init
	# TODO(mcsaucy): update this to test.sh once #67 is merged.
	PYTHONPATH=./Scraper pytest
