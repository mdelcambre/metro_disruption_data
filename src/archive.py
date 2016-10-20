#/usr/bin/env python3
"""Provies the classes to scrape the main Metro Disruption Site"""

__author__ = "Mark Delcambre"
__copyright__ = "Copyright 2016, Mark Delcambre"
__license__ = "MIT"
__version__ = "0.1"

__maintainer__ = "Mark Delcambre"
__email__ = "mark@delcambre.com"

# built-in
import csv
import re
# 3rd Party Requested
import requests
from bs4 import BeautifulSoup
# custom library
from .report import ReportScraper

# Base url of the archive webpage
BASE_URL = 'http://www.wmata.com/rail/service_reports/viewReportArchive.cfm'

id_regex = re.compile(r'(\d+)$')

class ArchiveScraper:
    """Class for scraping the archive pages to insert into the sqlitedb.

    Args:
        None

    Attributes:
        None
    """
    report = ReportScraper()

    def scrape(self, csv_file):
        """Public function to start the scraping process the master archive.

        Args:
            csv_file: file path to save the output

        Returns:
            bool, True on success and False on failure
        """
        # get reports from the archive
        archive = self._get_archive()
        if not archive:
            return False
        reports = self._parse_archive(archive)
        if not reports:
            return False
        with open(csv_file, 'w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                    ['time',
                    'direction',
                    'color',
                    'location',
                    'problem',
                    'delay (min)',
                    'full text'])
            for report in reports:
                for row in self.report.scrape(report[0], report[1]):
                    try:
                        csv_writer.writerow(row)
                    except:
                        pass

    def _get_archive(self):
        try:
            re = requests.get(BASE_URL, timeout=30)
            if not re.ok:
                print("[AS][_get_archive] status code bad: {}".
                        format(re.status_code))
                return False
        except requests.exceptions.RequestException as ex:
            print("[AS][_get_archive] download failed: {}".format(ex))
            return False
        return re.content

    def _parse_archive(self, raw_archive):
        soup = BeautifulSoup(raw_archive, "html.parser")
        raw = soup.select("#internal-col2 > div > div > div > ul > li > a")
        raw_lines = []
        for el in raw:
            match = id_regex.search(el.get('href', ''))
            if match:
                raw_lines.append((match.group(0), el.text))
        return raw_lines

if __name__ == "__main__":
    scraper = ArchiveScraper()
    scraper.scrape('test.csv')




