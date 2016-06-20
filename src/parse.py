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
    direction   = re.compile(r'A (\w+?)-bound'),
    color       = re.compile(r'bound (\w+?) Line train'),
    station     = re.compile(r'train at (\w+?) (?:was|had)'),
    formats     = (
        re.compile(r'(?P<reason>did not operate), resulting in a (?P<delay>\d+?)-minute')
        re.compile(r'was (?P<reason> was expressed for .+)')
        re.compile(r'as delayed (?P<delay>\d+?) minutes? due to (?P<reason>.+)')
        re.compile(r'was offloaded due to (?P<reason>[^.]+)\. Passengers experienced a (?P<delay>\d+?)-minute')
    )
)


