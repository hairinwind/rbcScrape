from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def run(): 
	url = "http://fundinfo.rbcgam.com/mutual-funds/rbc-funds/prices/default.fs"
	response = requests.get(url, verify=False)
	soup = BeautifulSoup(response.text, 'html5lib')
	tables = soup.body.find_all('table')

	data = []
	for table in tables: 
		for tr in table.tbody.find_all('tr'):
			cols = tr.find_all('td')
			rowData = [x.text.strip() for x in cols]
			data.append(rowData)
	
	labels = []
	for th in tables[0].thead.find_all('th'):
		labels.append(th.text.strip())

	df = pd.DataFrame.from_records(data, columns=labels)
	now = datetime.now().strftime("%Y-%m-%d")
	csvFileName = 'rbcFunds_{0}.csv'.format(now)
	df.to_csv(csvFileName, index=False)


if __name__=="__main__":
	scheduler = BlockingScheduler()
	scheduler.add_job(run, 'cron', day_of_week='1-5', hour=23, minute=0)
	scheduler.start()
	