from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from pemail import gmailapi 

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
	csvFileName = 'result/rbcFunds_{0}.csv'.format(now)
	df.to_csv(csvFileName, index=False)
	print('sending email...', [csvFileName])
	gmailapi.send('rbcFund','', files=[csvFileName])


if __name__=="__main__":
	runItNow = sys.argv[1] if len(sys.argv) >= 2 else None
	if runItNow and runItNow.upper() == 'NOW':
		run()
	else :
		print('run cron job...')
		scheduler = BlockingScheduler()
		scheduler.add_job(run, 'cron', day_of_week='1-5', hour=23, minute=0)
		scheduler.start()
	