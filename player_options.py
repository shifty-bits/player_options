import requests
import json
import urllib
import sys
from bs4 import BeautifulSoup


name = input("enter a player name: ")
if name:
	url = f"http://lookup-service-prod.mlb.com/json/named.search_player_all.bam?sport_code=\'mlb\'&name_part=\'{name.lower()}\'"

	r = requests.get(url)
	id = 0
	try:
		id = r.json()['search_player_all']['queryResults']['row']['player_id']
	except:
		print(f"could not find player: {name}")
		
	split_name = name.lower().split()
	mlb_file = requests.get(f'https://www.mlb.com/player/{split_name[0]}-{split_name[1]}-{id}')
	soup = BeautifulSoup(mlb_file.content, features='html.parser')
	table = soup.find( "table", {"class":"transactions-table"}) 

	option_years = []
	for row in table.findAll("tr")[1:]:
		elements = row.findAll("td")
		date = elements[1]
		action = elements[2]
		if 'optioned' in action.text and date.text.split()[-1] not in option_years:
			option_years.append(date.text.split()[-1])
	print(f"Option years: {option_years}")
else:
	print("no name entered")