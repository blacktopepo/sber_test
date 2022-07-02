import json
import re

import requests

from client import Client

client_soup = Client()


years = client_soup.years
regions = client_soup.regions

data = requests.post(f)