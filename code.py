import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.worldometers.info/coronavirus/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find(id='main_table_countries_today')

f = csv.writer(open("covid.csv", "w"))
f.writerow(["Country","Number of Cases","Number of deaths"])

count=0
for row in table.find_all('tr')[1:]:  
	if count <10:
		name = row.find('a')
		cases = row.find_all('td')[2].contents
		deaths = row.findAll('td')[4].contents
		if None in (name, cases, deaths):
			continue
		f.writerow([name.text.strip(),"".join(cases),"".join(deaths)])
		count+=1
	else:
		break
