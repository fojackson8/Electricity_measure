
from bs4 import BeautifulSoup
import requests
import numpy as np
import re
import urllib
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import datetime
from datetime import datetime as DT
import time

# Set name of URL from which to get files, and a unique identifier of the desired file on the site
myURL = "http://176.58.100.152/clamp/"
specific_file = "22204b07adff412"

# Only fetch visible data from the page, i.e. all filenames
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

soup = BeautifulSoup(requests.get(myURL).text, "lxml")

file_match = soup.findAll(href = re.compile(specific_file))
   
visible_texts = filter(visible, file_match)

# Turn extracted filenames into strings so that they can be handled
# with regexp search. This loop makes an array of strings, then extracts
# the specific substring of interest into a new array

all_files = []

for each_string in visible_texts:
    a = str(each_string)
    b = re.search('>(.+?)<', a)
    c = b.group(1)
    d = myURL + c
    all_files.append(d)
    

    

# Put the date selector here, so that only a subset of the files are fetched and parsed. 
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=7)

selector_string2 = end_date.strftime("%Y-%m-%d")
selector_string1 = start_date.strftime("%Y-%m-%d")

indexes1 = [i for i, x in enumerate(all_files) if selector_string1 in x]
indexes2 = [i for i, x in enumerate(all_files) if selector_string2 in x]

final_index = indexes1 + indexes2
index_range = np.linspace(final_index[1],final_index[0],final_index[1] - final_index[0] +1,dtype=int)
file_subset = (all_files[i] for i in index_range)


# Now filename is set, actually extract the csv from the site,
# and open here. Loop through the array of filenames in all_files,
# extracting the csv file for each, and appending the contained
# data to a new array

all_dates = []
all_values = []


for filename in file_subset:
    myfile = urllib.request.urlopen(filename)
    urllib.request.urlretrieve(filename, "temp.csv")
    e = pd.read_csv('temp.csv', names = ["Date","Value"])
    each_date = e.Date
    each_value = e.Value
    all_dates.extend(each_date)
    all_values.extend(each_value)

# Now convert all the dates in all_dates to numbers that matplotlib can
# understand and make plots with
all1 = []

for every_date in all_dates:
    f = DT.strptime(every_date, "%Y-%m-%d  %H:%M:%S")
    date_num = matplotlib.dates.date2num(f)
    all1.append(date_num)

    
plt.plot(all1, all_values)
ax = plt.gca()
xfmt = matplotlib.dates.DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
plt.gcf().autofmt_xdate()  
plt.xlabel('Time')
plt.ylabel('Relative Energy Usage')
plt.show()







