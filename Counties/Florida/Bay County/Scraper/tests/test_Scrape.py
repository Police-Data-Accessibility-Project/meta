import csv
import pytest
import unittest
import Scraper

@pytest.fixture(scope='module')
def testdatadir(request):
    # Get a py.path.local, which is a bit friendlier to work with.
    return request.fspath.join('..').join('testdata')

def csv2dictlist(csvfile):
    with open(csvfile, 'r') as w:
        dl = [r for r in csv.DictReader(w)]
        for d in dl:
            del d["_id"]  # this is random, so strip it for comparisons
        return dl

class TestScrape:

    def test_scrape(self, tmpdir, testdatadir):
        td = tmpdir.mkdir('scraper')
        outfile = td.join('bay-county-scraped.csv')
        wantfile = testdatadir.join('bay-county-scraped.csv.golden')

        # TODO(mcsaucy): refactor Scraper to use less global state.
        Scraper.settings['max-records'] = 3
        Scraper.settings['solve-captchas'] = True
        Scraper.settings['output'] = outfile
        Scraper.main()

        have = csv2dictlist(outfile)
        want = csv2dictlist(wantfile)

        for i in range(len(want)):
            # This gives us a cleaner diff to work with
            assert have[i] == want[i]
        # This is more complete.
        assert have == want

