---
title: "Webscraping using Beautifulsoup"
date: 2020-05-29T10:07:17+05:30
---

The data-rich internet is now the ground for a lot of research, and web scraping gives you the leverage to collect the information that suits your needs.
So, in this article we are going to use beautifulsoup - a popular python library for web scraping, and get some info on a familiar topic - the Covid-19 pandemic.

But before we dive in, let’s clear up some FAQs.

**Why Web Scraping?**

As we just discussed, the internet is overflowing with information. This data can be collected and processed to get meaningful insights. For example, you want to monitor your competitors pricing strategy in the e-commerce market or when you want to analyse the feedback on your product or gather stats for one of your studies. It is true that all this can be done manually, but why would you say no to something being automated right? 

**Is web scraping legal?**

This can’t be answered by a simple yes or a no. The data published by any website for public consumption is legal to scrape. But the way you plan to use this scrapped data is when the question of legality comes into picture. If this data is used for your personal use and analysis, then it is absolutely ethical. But in case you are using it for commercial purposes, you must reference the original website.

So, my fellow pythoneers, let’s buckle up and jump right in.


**Installing Beautiful soup**

Installing beautiful soup and the other required packages is absolutely effortless if you have a python installer like pip. Enter the following commands in the terminal to install beautiful soup and request libraries. Although we are going to use the csv library, we don’t have to explicitly install as it is included in the Python installation.


```
pip install beautifulsoup4
pip install requests

```



**Inspecting the web source**

So when we look at the source of any website, dynamic or static, all we see is chaos. There’s loads of HTML tags with tons of attributes and javascript adds to all that mess. And imagine extracting the data you need from that, phew! tiring. But have no worries 'cause, beautifulsoup makes your life a lot more easier as this package has innate functions that help you to traverse through HTML and XML documents. 

Okay so let's head over to the site https://www.worldometers.info/coronavirus/ 

Let's scrape the table below and get the 10 countries having the most number of cases. Right click on the page and select inspect or if you are using Chrome you can open the developer tools through the menu View —>Developer—> Developer tools. You have to hover on the HTML in the elements tab to see the corresponding element of the page highlight.

![Inspect elements Screenshot](/Inspect-screenshot.JPG)

Let’s get started with the code. Open up your favourite text editor and import the libraries.

```
import requests
from bs4 import BeautifulSoup
import csv
 
URL = 'https://www.worldometers.info/coronavirus/'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

```

 The above few lines of code, firstly it performs a HTTP request and retrieves the HTML of the given url. Then, an object of class beautifulsoup is created that takes the HTML contents. 

Always search for the id and name attributes, instead of class or styles, in the HTML tags as they are unique which can help us to access the data easily. Observe that the id for the table we want is 'main_table_countries_today’ and in the td tags of that table body contains the data we need. 

```
table = soup.find(id='main_table_countries_today')

```

When we call the find method, the entire HTML vis-à-vis the table with id = main_table_countries_today is in the variable table. You can print out the variable and check it out.
Now that we have accessed the table, all we need to do is access each row in it.

```
for row in table.findAll('tr')[1:]:  
		country = row.find('a')
		cases = row.findAll('td')[2].contents
		deaths = row.findAll('td')[4].contents

		print(country, “—>”, ””.join(cases),"".join(deaths)])

```

As you see this code calls the findAll() method which returns an iterable. Now if you observe the HTML, the first tr tag contains the heading for each column. So [1:] makes sure the first row is eliminated.

Using the same old find method to retrieve the name of the country. Notice that the name is differently tagged (using an anchor tag) than the other rows. 
We are going to parse the entire row and pick the columns we need and append those values in the lists - cases and deaths.

>NOTE: If you surf the net, you might find methods like find_all(), which is exactly same as findAll.The camel-cased versions ( findAll , findAllNext , nextSibling , etc.) have all been renamed to conform to the Python style guide, but the old names are still available in beautifulsoup 4 to make porting easier.


When you run the code, you’ll see the entire tag of the country being displayed. No worries, beautifulsoup has got you covered!. Use .text to strip off all that mess. Although you might see a lot of unnecessary spaces which you can eliminate using the method .strip().



```

for row in table.findAll('tr')[1:]:  
	country = row.find('a')
	cases = row.findAll('td')[2].contents
	deaths = row.findAll('td')[4].contents
	print(country.text.strip(), “—>”, ””.join(cases),"".join(deaths)])
```

Well, running this program, might give you an Attribute error - AttributeError: 'NoneType' object has no attribute 'text'. This is because of the None we have encountered previously. Add the below piece of code to overcome that error.

```

for row in table.findAll('tr')[1:]:  
	country = row.find('a')
	cases = row.findAll('td')[2].contents
	deaths = row.findAll('td')[4].contents
	if None in (name, cases, deaths):
		continue
	print(country.text.strip(), “—>”, ””.join(cases),"".join(deaths)])

```

Let’s add in a condition so as to get only the top ten countries and get rid of that huge amount of data overflowing our terminal. 

```

count=0
for row in table.find_all('tr')[1:]:  
	if count <10:
		name = row.find('a')
		cases = row.find_all('td')[2].contents
		deaths = row.findAll('td')[4].contents
		if None in (name, cases, deaths):
			continue
		print(country.text.strip(), “—>”, ””.join(cases),"".join(deaths)])
		count+=1
	else:
		break

```

**Writing into a csv file**

Now that we are successful in scrapping the site, let’s talk about the latter steps - Storing and analytics .

In this article, we are going to dump the scraped data into a csv (comma-separated values) file. We can open any csv file with any spreadsheet application like MS Excel, Google spreadsheets etc. This data can be easily visualised using charts to identify trends, patterns and anomalies. 

{{< gist don-bhavana 847dbb65d5e4c48e0223cd8d0eeb587a >}}

If you notice, we have opened a csv file in write mode. The first row is column labels by default. The writerow method takes only one argument, and hence we pass the list of items.


**Conclusion**

It is obvious that web scrapers can read and extract data from web pages more quickly than humans can, but care should be taken that the web scraping process does not affect the performance/bandwidth of the web server in any way. If it is disturbed, a lot of web servers automatically block your IP, preventing further access to that website. Although we can overcome this by using proxy IPs, which can also help in hiding your identity.

In this article, we have just discussed the basic usage of the beautifulsoup. To make a scrapper more efficient, we can add schedulers, rotating IPs, spoofing user agents and fail proofing  using message queues with the help of tools like scrappy, selenium, splinter etc.  
 
