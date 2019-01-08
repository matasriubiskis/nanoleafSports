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


'''returns the data on your nanoleaf'''
def info():
	ipAddress = '192.168.2.31'
	token = '1auzweH8pedNzJZHyPTP18V1MAey51Fd'
	#TODO: use nanoleaf-setup to automatically find the IPaddress and token

	return ipAddress, token



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
	
def main():
	team = "Boston Bruins"
	game = get_games(team)
	live = get_live(game.link)
	teamEffect = "Leafs"
	myAurora.on = True
	myAurora.brightness = 30
	myAurora.effect = teamEffect
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
					myAurora.effect = teamEffect
			sleep(5)

		except KeyboardInterrupt:
			myAurora.off = True
			os._exit(0)


#def parse_args(args):
	#TODO: Take in command line arguments (team and brightness)

#def select_team():
	#TODO: based on command line selection of team

#def setup():
	#TODO: make sure that nanoleaf knows the effects of each team
	

'''runs the goal light I just made my best guess at it so change if you want'''
def goal():
	myAurora.rgb = [255,0,0] #Red
	sleep(5) #5 seconds seemed like a good time for the red light to stay
	myAurora.rgb = [255,255,255] #White
	sleep(0.3)
	myAurora.rgb = [255,0,0]
	sleep(5)
	myAurora.rgb = [255,255,255]
	sleep(0.3)
	myAurora.rgb = [255,0,0]
	sleep(5)

'''Create link for the current games live feed'''
def get_live(url):
	default = "https://statsapi.web.nhl.com"
	liveURL = default + url
	return liveURL

if __name__ == '__main__':
	ipAddress, token = info()
	myAurora = Aurora(ipAddress, token)
	main()
	
	
	


