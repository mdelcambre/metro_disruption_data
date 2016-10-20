"Provides the functions for parsing the metro disruptions."

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
    station     = re.compile(r'train (?:at|outside) (.+?) (?:was|had|did)'),
    formats     = (
        re.compile(r'(?P<reason>did not operate), resulting in an? (?P<delay>\d+?)-minute'),
        re.compile(r'as delayed (?P<delay>\d+?) minutes? due to (?P<reason>.+)'),
        re.compile(r'due to (?P<reason>[^.]+)\..*?\.?\s+(?:Passengers|Customers) experienced an? (?P<delay>\d+?)-minute'),
        re.compile(r' for (?P<reason>schedule adherence/improved train spacing)\..*?\.?\s+(?:Passengers|Customers) experienced an? (?P<delay>\d+?)-minute'),
        re.compile(r'was (?P<reason>expressed for .+)'),
        re.compile(r'was (?P<reason>offloaded .+)'),
    )
)

def parse(disruption):
    """Function to parse the disruption strings into a tuple of data.
    Args:
        disruption (string)
    Returns:
        tuple of time, direction, color, station, reason, delay
    """
    try:
        group = regex_group.time.search(disruption)
        time = group.group(1)
        group = regex_group.direction.search(disruption)
        direction = group.group(1)
        group = regex_group.color.search(disruption)
        color = group.group(1)
        group = regex_group.station.search(disruption)
        station = group.group(1)
        reason = False
        for regex in regex_group.formats:
            group = regex.search(disruption)
            if group:
                reason = group.group('reason')
                try:
                    delay = group.group('delay')
                except IndexError:
                    delay = None
                break
        if not reason:
            return (time, '', '', '', '', '', disruption)
            print("no reason: {}".format(disruption))
        else:
            return (time, direction, color, station, reason, delay, disruption)
    except Exception as err:
        print("Unable to process: {}".format(disruption.encode('utf-8')))
        try:
            if time:
                return (time, '', '', '', '', '', disruption)
            return False
        except UnboundLocalError:
            return False

