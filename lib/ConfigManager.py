import configparser

class ConfigManager:
    def __init__(self, pluginDir):
        config = configparser.ConfigParser()
        config.read(pluginDir + '/config.ini')
        try:
            self.schemeYellow = config['GamesenseShiftlight']['scheme_yellow']
        except:
            self.schemeYellow = 'default'
        try:
            self.schemeRed = config['GamesenseShiftlight']['scheme_red']
        except:
            self.schemeRed = 'default'
        try:
            self.schemeOptimal = config['GamesenseShiftlight']['scheme_optimal']
        except:
            self.schemeOptimal = 'default'
        try:
            self.keepaliveTimeout = config.getint('GamesenseShiftlight', 'keepalive_timeout')
        except:
            self.keepaliveTimeout = 0