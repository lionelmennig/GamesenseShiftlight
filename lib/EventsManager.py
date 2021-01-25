import json

class EventsManager:

    def __init__(self, pluginDir, configManager):
        GAME_NAME = "ASSETTOCORSA"
        GAME_DISPLAY_NAME = "Assetto Corsa"
        DEVELOPER_NAME = "leeyo.be"
        YELLOW_EVENT_NAME = "YELLOWSHIFTLIGHT"
        RED_EVENT_NAME = "REDSHIFTLIGHT"
        OPTIMAL_EVENT_NAME = "OPTIMALSHIFTLIGHT"
    
        # Game's metadata
        self.gameMetadata = {"game": GAME_NAME, "game_display_name": GAME_DISPLAY_NAME, "developer": DEVELOPER_NAME}
        if (configManager.keepaliveTimeout >= 1 and configManager.keepaliveTimeout <= 60):
            self.gameMetadata["deinitialize_timer_length_ms"] = configManager.keepaliveTimeout * 1000 # seconds to milliseconds
            self.eventHeartbeat = {"game": GAME_NAME}
        
        # Binders finder
        with open(pluginDir + '/events/yellow/' + configManager.schemeYellow + '/YellowEventBinder.json') as f:
            self.yellowEventBinder = json.load(f)
            self.yellowEventBinder["game"] = GAME_NAME
            self.yellowEventBinder["event"] = YELLOW_EVENT_NAME
        
        if (configManager.schemeRed != "none"):
            with open(pluginDir + '/events/red/' + configManager.schemeRed + '/RedEventBinder.json') as f:
                self.redEventBinder = json.load(f)
                self.redEventBinder["game"] = GAME_NAME
                self.redEventBinder["event"] = RED_EVENT_NAME
        else:
            self.redEventBinder = None
        
        if (configManager.schemeOptimal != "none"):
            with open(pluginDir + '/events/optimal/' + configManager.schemeOptimal + '/OptimalEventBinder.json') as f:
                self.optimalEventBinder = json.load(f)
                self.optimalEventBinder["game"] = GAME_NAME
                self.optimalEventBinder["event"] = OPTIMAL_EVENT_NAME
        else:
            self.optimalEventBinder = None
            
        # Updater builder
        if (self.redEventBinder is None and self.optimalEventBinder is None):
            self.eventUpdater = {"game": GAME_NAME, "event": YELLOW_EVENT_NAME, "data": {"value": 0}}
        elif (self.redEventBinder is None):
            self.eventUpdater = {"game": GAME_NAME, "events": [{"event": YELLOW_EVENT_NAME, "data": {"value": 0}}, {"event": OPTIMAL_EVENT_NAME, "data": {"value": 0}}]} # Index 1 for "optimal" state when there is no "red" state
        elif (self.optimalEventBinder is None):
            self.eventUpdater = {"game": GAME_NAME, "events": [{"event": YELLOW_EVENT_NAME, "data": {"value": 0}}, {"event": RED_EVENT_NAME, "data": {"value": 0}}]} # Index 1 for "red" state when there is no "optimal" state
        else:
            self.eventUpdater = {"game": GAME_NAME, "events": [{"event": YELLOW_EVENT_NAME, "data": {"value": 0}}, {"event": RED_EVENT_NAME, "data": {"value": 0}}, {"event": OPTIMAL_EVENT_NAME, "data": {"value": 0}}]} # Index 1 for "red" state and index 2 for "optimal" state when both are active 
        
        # Event's utils finder
        try:
            eventUtilsModule = __import__('gamesense_shiftlight.events.yellow.' + configManager.schemeYellow + '.YellowEventUtils', fromlist=['YellowEventUtils'])
            self.yellowEventUtils = eventUtilsModule.YellowEventUtils
        except:
            eventUtilsModule = __import__('gamesense_shiftlight.lib.BaseEventUtils', fromlist=['BaseEventUtils'])
            self.yellowEventUtils = eventUtilsModule.BaseEventUtils
        if (self.redEventBinder is not None):
            try:
                eventUtilsModule = __import__('gamesense_shiftlight.events.red.' + configManager.schemeRed + '.RedEventUtils', fromlist=['RedEventUtils'])
                self.redEventUtils = eventUtilsModule.RedEventUtils
            except:
                eventUtilsModule = __import__('gamesense_shiftlight.lib.BaseEventUtils', fromlist=['BaseEventUtils'])
                self.redEventUtils = eventUtilsModule.BaseEventUtils
        if (self.optimalEventBinder is not None):
            try:
                eventUtilsModule = __import__('gamesense_shiftlight.events.optimal.' + configManager.schemeOptimal + '.OptimalEventUtils', fromlist=['OptimalEventUtils'])
                self.optimalEventUtils = eventUtilsModule.OptimalEventUtils
            except:
                eventUtilsModule = __import__('gamesense_shiftlight.lib.BaseOptimalEventUtils', fromlist=['BaseOptimalEventUtils'])
                self.optimalEventUtils = eventUtilsModule.BaseOptimalEventUtils
    
    def tryToLoadYellowOnly(self, yellowFloatValue, redFloatValue):
        if (self.redEventBinder is None and self.optimalEventBinder is None):
            if (redFloatValue > 0):
                yellowFloatValue = 100
            convertedYellowValue = self.yellowEventUtils.getConvertedValue(yellowFloatValue)
            if (self.yellowEventUtils.canIgnoreUpdatingCurrentValue() == False):
                self.eventUpdater["data"]["value"] = convertedYellowValue
                return True
        return False
    
    def tryToLoadYellowAndOptimal(self, yellowFloatValue, optimalShiftlightState):
        if (self.redEventBinder is None):
            convertedYellowValue = self.yellowEventUtils.getConvertedValue(yellowFloatValue)
            convertedOptimalValue = self.optimalEventUtils.getConvertedValue(optimalShiftlightState)
            if (self.yellowEventUtils.canIgnoreUpdatingCurrentValue() == False or convertedOptimalValue != self.eventUpdater['events'][1]['data']['value']):
                self.eventUpdater['events'][0]['data']['value'] = convertedYellowValue
                self.eventUpdater['events'][1]['data']['value'] = convertedOptimalValue
                return True
        return False
    
    def tryToLoadYellowAndRed(self, yellowFloatValue, redFloatValue):
        if (self.optimalEventBinder is None):
            convertedYellowValue = self.yellowEventUtils.getConvertedValue(yellowFloatValue)
            convertedRedValue = self.redEventUtils.getConvertedValue(redFloatValue)
            if (self.yellowEventUtils.canIgnoreUpdatingCurrentValue() == False or self.redEventUtils.canIgnoreUpdatingCurrentValue() == False):
                self.eventUpdater['events'][0]['data']['value'] = convertedYellowValue
                self.eventUpdater['events'][1]['data']['value'] = convertedRedValue
                return True
        return False
    
    def tryToLoadAllEvents(self, yellowFloatValue, redFloatValue, optimalShiftlightState):
        convertedYellowValue = self.yellowEventUtils.getConvertedValue(yellowFloatValue)
        convertedRedValue = self.redEventUtils.getConvertedValue(redFloatValue)
        convertedOptimalValue = self.optimalEventUtils.getConvertedValue(optimalShiftlightState)
        if (self.yellowEventUtils.canIgnoreUpdatingCurrentValue() == False or self.redEventUtils.canIgnoreUpdatingCurrentValue() == False or convertedOptimalValue != self.eventUpdater['events'][2]['data']['value']):
            self.eventUpdater['events'][0]['data']['value'] = convertedYellowValue
            self.eventUpdater['events'][1]['data']['value'] = convertedRedValue
            self.eventUpdater['events'][2]['data']['value'] = convertedOptimalValue
            return True
        return False