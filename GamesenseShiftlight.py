################################################
# GamesenseShiftlight by Lionel Mennig (leeyo)
# 
# Version: 1.0.0
# Based on Sidekick 1.11.1 (thanks to Topuz)
#
# None of the code below is to be redistributed
# or reused without the permission of the
# author(s).
################################################

import os, sys
from os import path
import json
from gamesense_shiftlight.lib import requests
from gamesense_shiftlight.lib.continuous_threading import OperationThread
from gamesense_shiftlight.lib.GamesenseEnvironment import GamesenseEnvironment
from gamesense_shiftlight.lib.ConfigManager import ConfigManager
from gamesense_shiftlight.lib.EventsManager import EventsManager
from gamesense_shiftlight.lib.OptimalShiftlightState import OptimalShiftlightState
from gamesense_shiftlight.lib.HeartbeatTriggerer import HeartbeatTriggerer

class GamesenseShiftlight:
    
    # Useful vars
    pluginDir = os.path.dirname(__file__) # Finding plugin directory
    headers = {'Content-Type': 'application/json'} # Required to call 'requests.post()' with 'data' param (pre 'json' version)
    
    # Helpers
    configManager = ConfigManager(pluginDir) # Containing config.ini parsed parameters
    gamesenseEnvironment = GamesenseEnvironment() # Containing API's URLs
    eventsManager = EventsManager(pluginDir, configManager) # Containing binders, updaters and their utils
    
    # Loading GameSense's metadata and events binders
    requests.post(gamesenseEnvironment.urlToMetadata, data = json.dumps(eventsManager.gameMetadata), headers = headers)
    requests.post(gamesenseEnvironment.urlToBind, data = json.dumps(eventsManager.yellowEventBinder), headers = headers)
    if (eventsManager.redEventBinder is not None):
        requests.post(gamesenseEnvironment.urlToBind, data = json.dumps(eventsManager.redEventBinder), headers = headers)
    if (eventsManager.optimalEventBinder is not None):
        requests.post(gamesenseEnvironment.urlToBind, data = json.dumps(eventsManager.optimalEventBinder), headers = headers)
    
    # Handling the "Keepalive heartbeat"
    if (configManager.keepaliveTimeout >= 1 and configManager.keepaliveTimeout <= 60):
        keepaliveTimeout = configManager.keepaliveTimeout * 0.9 # Reduce value by 10% to avoid triggering heartbeat too late
        heartbeatTriggerer = HeartbeatTriggerer(keepaliveTimeout, gamesenseEnvironment.urlToKeepalive, eventsManager.eventHeartbeat, headers)
        heartbeatTriggerer.daemon = True # Daemon set to true will kill the thread once main program exits
        heartbeatTriggerer.start()
        
    # Creating OperationThreads to handle simultaneous POST requests
    availableThreads = []
    if (eventsManager.redEventBinder is not None):
        threadsCount = eventsManager.yellowEventUtils.getNumberOfRequiredThreads() + eventsManager.redEventUtils.getNumberOfRequiredThreads()
    else:
        threadsCount = eventsManager.yellowEventUtils.getNumberOfRequiredThreads()
    for i in range(threadsCount):
        operationThread = OperationThread(target = lambda url, data, headers : requests.post(url, data = json.dumps(data), headers = headers))
        operationThread.daemon = True # Daemon set to true will kill the thread once main program exits
        operationThread.start()
        availableThreads.append(operationThread)

    threadsIterator = 0
    def __getAvailableThread(self):
        if (self.threadsIterator == self.threadsCount):
            self.threadsIterator = 0
        self.threadsIterator += 1
        return self.availableThreads[self.threadsIterator - 1]
    
    # Updating method
    def update(self, yellowFloatValue = 0, redFloatValue = 0, optimalShiftlightState = OptimalShiftlightState.OFF):
        if (self.eventsManager.tryToLoadYellowOnly(yellowFloatValue, redFloatValue)):
            self.__getAvailableThread().add_data(self.gamesenseEnvironment.urlToUpdate, self.eventsManager.eventUpdater, self.headers)
        elif (self.eventsManager.tryToLoadYellowAndOptimal(yellowFloatValue, optimalShiftlightState)):
            self.__getAvailableThread().add_data(self.gamesenseEnvironment.urlToUpdateMulti, self.eventsManager.eventUpdater, self.headers)
        elif (self.eventsManager.tryToLoadYellowAndRed(yellowFloatValue, redFloatValue)):
            self.__getAvailableThread().add_data(self.gamesenseEnvironment.urlToUpdateMulti, self.eventsManager.eventUpdater, self.headers)
        elif (self.eventsManager.tryToLoadAllEvents(yellowFloatValue, redFloatValue, optimalShiftlightState)):
            self.__getAvailableThread().add_data(self.gamesenseEnvironment.urlToUpdateMulti, self.eventsManager.eventUpdater, self.headers)