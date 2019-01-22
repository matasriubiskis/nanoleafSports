# nanoleafSports
A python script to control your [Nanoleaf Aurora](https\://nanoleaf.me/en/), it will turn on the lights, configure the patern to your selected team's colours, and then pulse red when goals are scored. (currently only NHL)

## Requirements
* Python 3.6+
* [Python interface for Nanoleaf](https://github.com/software-2/nanoleaf)
* Requests 

## Usage
* Put your Nanoleaf's IP address and token into the info function
* Replace Toronto Maple Leafs with the desired team name
* Change the effect
* Run the python script as normal `python3 nanoleafNHL.py`
* `Ctrl + C` to exit

## API Source
* [Schedule](https://statsapi.web.nhl.com/api/v1/schedule)
* [Live Game Data Example](https://statsapi.web.nhl.com/api/v1/game/2018020629/feed/live)

## Adding/Selecting Teams
* yaml files currently exist for several teams where I did my best to create colour schemes, if you believe they can be better please feel free to change them
* To add a team, create a yaml in the same format as the other ones, change the name and effect name, then edit the palette
* Add the full team name and yaml name to the select_team() function
* For now, to change the team just comment out the current team and un-comment your team

## License
[MIT License](http://opensource.org/licenses/MIT)

## TODO:
* Finish adding all the team colour schemes
* Allow for team selection at commandline
* Create setup function that finds the IP and token of your nanoleaf for you
