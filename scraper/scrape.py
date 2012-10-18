import argparse
from bs4 import BeautifulSoup
import json
import re
import urllib

URL_SCHEME = "http://voterguide.sos.ca.gov/propositions/%d/"
PROP_RANGE = range(30, 40 + 1)

class Proposition:
	def __init__(self):
		self.data = {}

	def update_with_html(self, html, url):
		soup = BeautifulSoup(html)
		
		# Get title
		content = soup.find('div', class_="propName")
		title = content.get_text()
		assert len(title) > 0

		# Get arguments
		content = soup.find(id = "contentPadding")
		paragraphs = content.find_all('p')
		assert len(paragraphs) is 5, "Expected 5 pargraphs, got %d." % len(paragraphs)
		
		summary = Proposition.strip_bs4_paragraph(paragraphs[0])
		yes_means = Proposition.strip_bs4_paragraph(paragraphs[1])
		no_means = Proposition.strip_bs4_paragraph(paragraphs[2])
		yes_arg = Proposition.strip_bs4_paragraph(paragraphs[3])
		no_arg = Proposition.strip_bs4_paragraph(paragraphs[4])

		# Get yes and no arguments
		contact_divs = content.find_all("div", class_ = "grid_8")
		assert len(contact_divs) is 2

		for_contact = str(contact_divs[0].dl)
		no_contact = str(contact_divs[1].dl)

		# Assign data
		self.data = {
			"title" : title,
			"summary" : summary,
			"yes_means" : yes_means,
			"no_means" : no_means,
			"yes_arg" : yes_arg,
			"no_arg" : no_arg,
			"yes_contact" : for_contact,
			"no_contact" : no_contact,
			"url" : url
		}

	@staticmethod
	def strip_bs4_paragraph(p):
		strip_chars = re.compile("[\n\r\t]")

		# Remove contained <span> tags that aren't relevant.
		for span in p.find_all('span'):
			span.decompose()

		text = p.get_text()
		text = re.sub(strip_chars, "", text)

		return text

	def json(self):
		return json.dumps(self.data)

	def json_pretty(self):
		return json.dumps(self.data, sort_keys=True, indent=4)


def scrape_props(file):
	result = {}

	for prop_number in PROP_RANGE:
		url = URL_SCHEME % prop_number
		html = download_page(url)
		prop = Proposition()
		prop.update_with_html(html, url)

		result[prop_number] = prop.data

		if not file:
			print "Prop %d: " % prop_number, prop.json_pretty()

	if file:
		f = open(file, 'w')
		f.write(json.dumps(result, sort_keys=True, indent=4))
		f.close()

def download_page(url):
	file_handle = urllib.urlopen(url)
	return file_handle.read()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Scrape propositions and output to a JSON file.')
	parser.add_argument('--file', required=False)
	args = parser.parse_args()
	scrape_props(args.file if "file" in args else None)