class RpmConverter:
    def getShiftlightPercentage(self, rpmPercentageValue, lowerLimitPercentage, higherLimitPercentage):
        total = higherLimitPercentage - lowerLimitPercentage # Representing 100%
        value = rpmPercentageValue - lowerLimitPercentage # Representing the value of the percentage
        return (value / total) * 100