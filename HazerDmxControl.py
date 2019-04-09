from DmxPy import DmxPy 

class HazerDmxControl:
    def __init__(self, serialPort):
        self.dmx = DmxPy(serialPort)
        self.hazeChannel = 1
        self.fanChannel = 2
        
    
    def _percentToDMXRange(self, percentage):
        return int(round( (percentage / 100.0) * 255))
        
    def _calcAndSend(self, channel, percentage):
        self.dmx.setChannel(channel, self._percentToDMXRange(percentage))
        print("Sending to channel: ", channel ," percentage: ", percentage ," dmx range:", self._percentToDMXRange(percentage) )
        self.dmx.render()   
        
    def setHazeIntensity(self, hazePercentage):
        self._calcAndSend(self.hazeChannel, hazePercentage)
        
    def setFanSpeed(self, fanPercentage):
        self._calcAndSend(self.fanChannel, fanPercentage)
        
