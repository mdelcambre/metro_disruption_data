"Provides the class for parsing the metro"

__author__ = "Mark Delcambre"
__copyright__ = "Copyright 2016, Mark Delcambre"
__license__ = "MIT"
__version__ = "0.1"

__maintainer__ = "Mark Delcambre"
__email__ = "mark@delcambre.com"

# built-in
from argparse import Namespace
import re

# regex
regex_group = Namespace(
    time        = re.compile(r'^(\d{1,2}:\d\d (?:a\.m\.|p\.m\.))'),
    direction   = re.compile(r'A (.+?)-bound'),
    color       = re.compile(r'bound (\w+?) Line train'),
    station     = re.compile(r'train at (.+?) (?:was|had|did)'),
    formats     = (
        re.compile(r'(?P<reason>did not operate), resulting in a (?P<delay>\d+?)-minute'),
        re.compile(r'(?P<reason>was expressed for .+)'),
        re.compile(r'as delayed (?P<delay>\d+?) minutes? due to (?P<reason>.+)'),
        re.compile(r'was offloaded due to (?P<reason>[^.]+)\. Passengers experienced a (?P<delay>\d+?)-minute')
    )
)

def parse(disruption):
    group = regex_group.time.search(disruption)
    time = group.group(1)
    group = regex_group.direction.search(disruption)
    direction = group.group(1)
    group = regex_group.color.search(disruption)
    color = group.group(1)
    group = regex_group.station.search(disruption)
    station = group.group(1)
    for regex in regex_group.formats:
        group = regex.search(disruption)
        if group:
            reason = group.group('reason')
            try:
                delay = group.group('delay')
            except IndexError:
                delay = None
            break
    print(time, direction, color, station, reason, delay)



if __name__ == "__main__":
    parse("6:40 a.m. A Greenbelt-bound Yellow Line train at Archives was offloaded due to a brake problem. Passengers experienced a 6-minute delay.")
    parse("9:11 a.m. A Mt. Vernon Square-bound Yellow Line train at Huntington did not operate, resulting in a 6-minute gap in service.")
    parse("12:18 p.m. A Greenbelt-bound Green Line train at Congress Heights was delayed 4 minutes due to a door problem.")
    parse("3:22 p.m. A Glenmont-bound Red Line train at Takoma was expressed for schedule adherence/improved train spacing.")



