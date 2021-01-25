import math

class BaseEventUtils:
    def getConvertedValue(floatValue):
        return math.ceil(floatValue)
    
    def getNumberOfRequiredThreads():
        return 4
    
    def canIgnoreUpdatingCurrentValue():
        return False