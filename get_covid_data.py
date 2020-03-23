import os

import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


print('Downloading HTML...')
r = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQU0SIALScXx8VXDX7yKNKWWPKE1YjFlWc6VTEVSN45CklWWf-uWmprQIyLtoPDA18tX9cFDr-aQ9S6/pubhtml#')
contents = r.text

soup = BeautifulSoup(contents, 'html5lib')

table = soup.find("table", attrs={ "class" : "waffle"})

table_body = table.find('tbody')

rows = table_body.find_all('tr')[3:]

df = pd.DataFrame()

print('Reading records...')

for row in tqdm(rows):
	cols = row.find_all('td')

	if cols[19].text.strip() == '1':
		outcome = 'died'
	elif cols[20].text.strip() == '1':
		outcome = 'recovered'
	else:
		outcome = 'NA'

	record = {'country': cols[6].text.strip(), 'age': cols[8].text.strip(), 'outcome': outcome}
	# print(record)
	df = df.append(record, ignore_index=True)

df.to_csv(os.path.join('data', 'COVID-19_patient_record.csv'), index=False)