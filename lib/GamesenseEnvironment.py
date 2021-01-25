from os import path
import json

class GamesenseEnvironment:

    def __init__(self):
        # GameSense's 'coreProps.json' finder and URLs mapper
        corePropsDir = path.expandvars(r'%PROGRAMDATA%/SteelSeries/SteelSeries Engine 3/')
        with open(corePropsDir + 'coreProps.json') as f:
            corePropsData = json.load(f)
        url = 'http://' + corePropsData['address'] + '/'
        
        self.urlToBind = url + 'bind_game_event'
        self.urlToRegister = url + 'register_game_event'
        self.urlToRemoveEvent = url + 'remove_game_event'
        self.urlToRemoveGame = url + 'remove_game'
        self.urlToUpdate = url + 'game_event'
        self.urlToUpdateMulti = url + 'multiple_game_events'
        self.urlToMetadata = url + 'game_metadata'
        self.urlToKeepalive = url + 'game_heartbeat'