import json
import re
from bs4 import BeautifulSoup

data = """ your HTML here"""
soup = BeautifulSoup(data, "html.parser")
pattern = re.compile(r"window.Rent.data\s+=\s+(\{.*?\});\n")
script = soup.find("script", text=pattern)
data = pattern.search(script.text).group(1)
data = json.loads(data)
print(data)
