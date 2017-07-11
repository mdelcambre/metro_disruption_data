#/usr/bin/env python3
"""Provies the classes to scrape the main Metro Disruption Site"""

__author__ = "Mark Delcambre"
__copyright__ = "Copyright 2016, Mark Delcambre"
__license__ = "MIT"
__version__ = "0.1"

__maintainer__ = "Mark Delcambre"
__email__ = "mark@delcambre.com"

# 3rd Party Requested
import requests
from bs4 import BeautifulSoup

from .parse import parse

#Acrhive report report url


# The base url for the individual reports
REPORT_URL = 'https://www.wmata.com/service/daily-report/daily-service-report.cfm?id='

class ReportScraper:
    """Class for scraping individual reports by id to insert into the sqlitedb.

    Args:
        None

    Attributes:
        None
    """

    def scrape(self, id, date):
        """Public function to start the scraping process for each report.

        Args:
            id (int): the report id that we are scraping (in the url)

        Returns:
            bool, True on success and False on failure
        """
        # first get report html
        raw_report = self._get_report(id)
        if not raw_report:
            print("[ReportScraper] Report {} failed to scrape".
                    format(id))
            return False
        # next parse report
        raw_disruptions = self._parse_html(raw_report)
        if not raw_disruptions:
            print("[ReportScraper] Report {} failed to parse".
                    format(id))
        disruptions = []
        for disrup in raw_disruptions:
            disruption = parse(disrup)
            if disruption:
                disruptions.append(
                        ("{} {}".format(date, disruption[0]),) + \
                                disruption[1:])
        return disruptions


    def _get_report(self, id):
        url = REPORT_URL + str(id)
        try:
            re = requests.get(url, timeout=30)
            if not re.ok:
                print("[RS][_get_report] status code bad: {}".
                        format(re.status_code))
                return False
        except requests.exceptions.RequestException as ex:
            print("[RS][_get_report download failed: {}".format(ex))
            return False
        return re.content

    def _parse_html(self, raw_report):
        soup = BeautifulSoup(raw_report, "html.parser")
        raw = soup.select("#cs_control_2897")
        raw_lines = []
        for text in raw[0].prettify().split('\n'):
            clean = text.strip()
            if not clean == '' and not clean[0] == '<' and not clean[0:5] == 'Daily':
                raw_lines.append(clean)
        return raw_lines


if __name__ == "__main__":
    scraper = ReportScraper()
    print(scraper.scrape(20170710100901, 'July 09, 2017'))



