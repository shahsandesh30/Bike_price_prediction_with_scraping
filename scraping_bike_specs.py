from urllib.request import urlopen 
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

class Scraper:
	def __init__(self):
		# initialize url
		self.web_url =  'https://www.carandbike.com/new-bikes/models'
		self.html_code = urlopen(self.web_url).read()
	
	def get_bike_urls(self):
		soup = BeautifulSoup(self.html_code, 'html.parser')
		
		bikes_div = soup.find('div', {'id':'newbike-pager'})
		bikes = bikes_div.find_all('a',{'class':'newmodel-bike__link h__block h__mb10 js-cty-url-new'}, href=True)
		
		bike_urls = []
		for bike in bikes:
			bike_urls.append(bike['href'])
		return bike_urls

	def get_bike_info(self, urls):
		url_count = 0
		bike_specs = []
		bikes_price = []
		for url in urls:
			html_code = urlopen(str(url)).read()
			soup = BeautifulSoup(html_code, 'html.parser')

			# getting the bike specs defined tag
			features = soup.find('div', {'class':'spec-hlist'})
			bike_overviews = features.find_all('li')

			# returns iteration object
			data_iterator = iter(bike_overviews)
			while True:
				try:
					# Getting only specification values
					Engine_Capacity = next(data_iterator).text.replace('Engine Capacity', '').strip() 
					Max_power = next(data_iterator).text.replace('Max Power', '').strip()
					Mileage = next(data_iterator).text.replace('Mileage', '').strip()
					Starting_Mechanism = next(data_iterator).text.replace('Starting Mechanism', '').strip()
					Ignition = next(data_iterator).text.replace('Ignition', '').strip()
					Gears = next(data_iterator).text.replace('Gears', '').strip()
					
					bike_specs.append([Engine_Capacity,
								Max_power,
								Mileage,
								Starting_Mechanism,
								Ignition,
								Gears
								])

				except StopIteration:
					break

			# price defined tag and get values
			bike_price = soup.find('span', {'id':'ex-showroom-price'}).text.replace(',','')
			bikes_price.append(bike_price)

		return bike_specs, np.array(bikes_price).reshape(-1,1)
		

	def into_csv_file(self, data, bikes_price):
		col_names = ['Engine_Capacity', 'Max_Power', 'Mileage', 'Starting_Mechanism', 'Ignition', 'Gears', 'Price']
		df = pd.DataFrame(np.column_stack([data, bikes_price]), columns=col_names)
		df.to_csv('bike_specs.csv', index=False)

if __name__ == '__main__':
	s = Scraper()
	bike_urls = s.get_bike_urls()
	bike_specs, bikes_price = s.get_bike_info(bike_urls)
	s.into_csv_file(bike_specs, bikes_price)
