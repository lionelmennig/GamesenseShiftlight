from gamesense_shiftlight.lib.OptimalShiftlightState import OptimalShiftlightState

class BaseOptimalEventUtils:
    def getConvertedValue(optimalShiftlightState):
        if (optimalShiftlightState == OptimalShiftlightState.OPTIMAL):
            return 1
        if (optimalShiftlightState == OptimalShiftlightState.OPTIMAL_LATE):
            return 2
        return 0