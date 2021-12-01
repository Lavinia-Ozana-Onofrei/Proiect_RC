import time


class Sender:
    def __init__(self, IpSender, PortSender, IpReceiver, PortReceiver, Timeout, WinSize, PackSize, Failure, fileName):
        self.IpSender = IpSender
        self.PortSender = PortSender
        self.IpReceiver = IpReceiver
        self.PortReceiver = PortReceiver
        self.Timeout = Timeout
        self.WinSize = WinSize
        self.PackSize = PackSize
        self.Failure = Failure
        self.fileName = fileName
        self.log = open('log.txt', 'w')

    def writeLog(self, msg):
        self.log.write(time.strftime('%d.%m.%Y   %H:%M:%S') + ':      ' + msg + '\n')
