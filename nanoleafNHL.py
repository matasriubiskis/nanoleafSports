#!/usr/bin/env python3

import json
from time import sleep
import sys
import requests
import datetime
import os
import itertools
from nanoleaf import setup
from nanoleaf import Aurora
import argparse
import yaml


#Constants
RED = [255,0,0]
WHITE = [255,255,255]



'''returns the data on your nanoleaf'''
def get_nanoleaf():
	address = "address.yaml"
	data = open(address,'r')
	result = yaml.load(data)
	return result['ipAddress'], result['token']

class Game:
	def __init__(self, game_info):
		self.link  = game_info['link']
		self.date  = game_info['gameDate']
		self.away  = game_info['teams']['away']['team']['name']
		self.home  = game_info['teams']['home']['team']['name']


'''gets the json response'''
def get_data(url):
	response = requests.get(url)
	response = response.json()
	return response

'''Returns the pk for the game, might need to add a check for multiple games
as back to back games might appear'''
def get_games(team):
	url = "https://statsapi.web.nhl.com/api/v1/schedule" 
	data = get_data(url)
	for game_info in data['dates'][0]['games']:
		game = Game(game_info)
		if team in game.away or team in game.home:
			return game


'''Create link for the current games live feed'''
def get_live(url):
	default = "https://statsapi.web.nhl.com"
	liveURL = default + url
	return liveURL
	

def main():
	team = select_team()[0]
	game = get_games(team)
	live = get_live(game.link)
	teamEffect = load_yaml(select_team()[1])
	myAurora.on = True
	myAurora.brightness = 30
	myAurora.effect_set_raw(teamEffect)
	allPlays = 0
	while True:
		try:
			data = get_data(live)
			plays = data['liveData']['plays']['allPlays']
			if len(plays) > allPlays:
				allPlays = len(plays)
				print(plays[len(plays)-1])
				print(datetime.datetime.now().time())
				currentPlay = plays[len(plays)-1]
				if currentPlay['result']['event'] == "Goal" and currentPlay['team']['name'] == team:
					goal()
					myAurora.effect_set_raw(teamEffect)
					myAurora.brightness = 30
			sleep(5)

		except KeyboardInterrupt:
			myAurora.off = True
			os._exit(0)


#def parse_args(args):
	#TODO: Take in command line arguments (team and brightness)

''' For now, uncomment the team that you want the lights to run for'''
def select_team():
	team = ["Toronto Maple Leafs" , "leafs.yaml"]
	#team = ["Calgary Flames" , "flames.yaml"]
	#team = ["Boston Bruins" , "bruins.yaml"]
	#team = ["Montreal Canadians" , "canadians.yaml"]
	#team = ["Detroit Red Wings", "wings.yaml"]
	return team

#def setup():
	#TODO: make sure that nanoleaf knows the effects of each team
	

'''runs the goal light I just made my best guess at it so change if you want'''
def goal():
	myAurora.rgb = RED #Red
	sleep(4) #4 seconds seemed like a good time for the red light to stay
	myAurora.rgb = WHITE #White
	sleep(0.3)
	myAurora.rgb = RED
	sleep(4)
	myAurora.rgb = WHITE
	sleep(0.3)
	myAurora.rgb = RED
	sleep(4)

def load_yaml(name):
    location = "effects/" + name
    data = open(location,'r')
    result = yaml.load(data)
    return result

if __name__ == '__main__':
	ipAddress, token = get_nanoleaf()
	myAurora = Aurora(ipAddress, token)
	main()
	
	
	


