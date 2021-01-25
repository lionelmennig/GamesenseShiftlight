from gamesense_shiftlight.lib.BaseEventUtils import BaseEventUtils

class RedEventUtils(BaseEventUtils):
    
    __lastConvertedValues = [0, 0, 0]
    def __addConvertedValue(newValue):
        __lastConvertedValues[2] = __lastConvertedValues[1]
        __lastConvertedValues[1] = __lastConvertedValues[0]
        __lastConvertedValues[0] = newValue
    
    def getConvertedValue(floatValue):
        convertedValue = super().getConvertedValue(floatValue)
        __addConvertedValue(convertedValue)
        return convertedValue
    
    def getNumberOfRequiredThreads():
        return 1

    def canIgnoreUpdatingCurrentValue():
        return (__lastConvertedValues[0] == 0 and __lastConvertedValues[1] == 0 and __lastConvertedValues[2] == 0)
            or (__lastConvertedValues[0] > 0 and __lastConvertedValues[0] <= 100 and __lastConvertedValues[1] > 0 and __lastConvertedValues[1] <= 100 and __lastConvertedValues[2] > 0 and __lastConvertedValues[2] <= 100)