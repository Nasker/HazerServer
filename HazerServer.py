import OSC
import sys
from multiprocessing import Process
from time import sleep
from HazerDmxControl import HazerDmxControl

server = OSC.OSCServer( ("0.0.0.0", 9000) )
server.timeout = 0
run = True

dmxControl = HazerDmxControl("/dev/ttyUSB0")

def handleTimeout(self):
    self.timed_out = True

# funny python's way to add a method to an instance of a class
import types
server.handleTimeout = types.MethodType(handleTimeout, server)

def userCallback(path, tags, args, source):
    print ("-Receiving: "+path+"\t"+tags+"\t",args)
    
    
def hazeIntensityCallback(path, tags, args, source):
    print "-Receiving: "+path+"\t"+tags+"\t",args[0]
    dmxControl.setHazeIntensity(args[0])
    
def hazeSpeedCallback(path, tags, args, source):
    print "-Receiving: "+path+"\t"+tags+"\t",args[0]
    dmxControl.setFanSpeed(args[0])

def quitCallback(path, tags, args, source):
    # don't do this at home (or it'll quit blender)
    global run
    run = False

server.addMsgHandler( "/haze/intensity", hazeIntensityCallback )
server.addMsgHandler( "/haze/speed", hazeSpeedCallback )
server.addMsgHandler( "/quit", quitCallback )

def eachFrame():
    print("Starting Server!")
    while run:
    # clear timed_out flag
        sleep(0.1)
        server.timed_out = False
        # handle all pending requests then return
        while not server.timed_out:
            server.handle_request()

try:
    eachFrameThread = Process(target=eachFrame)
    #readnSendCCSPrimaThread = Process(target=readnSendCCSPrima)
    eachFrameThread.start()
    #readnSendCCSPrimaThread.start()
    eachFrameThread.join()
    #readnSendCCSPrimaThread.join()
except(KeyboardInterrupt, SystemExit): 
    server.close()