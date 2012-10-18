props
-----
A tool for sharing your California Proposition selections. The data comes from the CA voter guide: 
http://voterguide.sos.ca.gov/propositions.

<strong>(This is still a work in progress.)</strong>

Components
----------
* <code>app/</code>

The proposition app itself. It's a python flask webserver the can be hosted so users can submit and share 
their opinons on california propositions.

* <code>scraper/</code>

Scrapes proposition information used for this app from the <a href="http://voterguide.sos.ca.gov/propositions">
CA Voter Guide</a>.

Dependencies
------------
* <code>app/</code>
  * <a href="https://github.com/mitsuhiko/flask">Flask</a>
* <code>scraper/</code>
  * <a href="http://www.crummy.com/software/BeautifulSoup/">beautifulsoup4</a>