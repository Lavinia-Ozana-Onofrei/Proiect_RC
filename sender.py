import time
import socket

FRAME_INFORMATION = 8
FRAME_DATA = 4
FRAME_ACKNOWLEDGE = 2

global nRead
global packetsLeftToSend
global packetsLeftToReceive


class Sender:
    def __init__(self, IpSender, PortSender, IpReceiver, PortReceiver, Timeout, WinSize, PackSize, Failure, fileName):
        self.IpSender = IpSender
        self.PortSender = int(PortSender)
        self.IpReceiver = IpReceiver
        self.PortReceiver = int(PortReceiver)
        self.Timeout = int(Timeout)
        self.WinSize = WinSize
        self.PackSize = 1500
        self.Failure = Failure
        self.fileName = fileName
        self.nrOfPackets = 0
        self.nrOfPacketsConf = 0
        self.fileLength = None
        self.file = None
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.IpSender, self.PortSender))
        self.log = open('log.txt', 'w')

    #  Realizează citirea fișierului selectat pentru trimitere și determină numărul de pachete în care este împărțit fișierul;
    def readFile(self):
        self.file = open(self.fileName, "rb")
        self.file.seek(0, 2)
        self.fileLength = self.file.tell()
        self.file.seek(0, 0)
        self.nrOfPackets = int(self.fileLength / self.PackSize)
        if self.fileLength % self.PackSize:
            self.nrOfPackets += 1

    #   Se ocupă cu trimiterea pachetului ce conține informații despre transfer:
    # primul câmp reprezintă tipul pachetului, al doilea numărul de pachete,
    # al treilea portul pe care aplicația de trimitere așteptă pachetele de confirmare și numele fișierului;
    def sendInfo(self):
        header = FRAME_INFORMATION
        firstFrame = b''
        firstFrame += header.to_bytes(1, "big")
        firstFrame += self.nrOfPackets.to_bytes(4, "big")
        firstFrame += self.PortSender.to_bytes(2, "big")
        firstFrame += self.fileName[self.fileName.rfind("/") + 1:].encode("UTF-8")
        self.sock.sendto(firstFrame, (self.IpReceiver, self.PortReceiver))
        self.writeLog(f'S-a trimis pachetul de informatii. Datele fisierului:')
        self.writeLog(f'Nume fisier: {self.fileName[self.fileName.rfind("/") + 1:]}')
        self.writeLog(f'Numar de pachete:  {str(self.nrOfPackets)}')

    #    Realizează efectiv transferul care este realizat după cum urmează:
    #  inițial se trimit un număr de pachete egal cu dimensiunea ferestrei
    #  după care se așteaptă primirea pachetelor de confirmare.
    #  Dacă recepția nu se realizează într-un anumit interval de timp se transferă din nou toate pachetele din fereatră.
    #  Pe masură ce se primesc pachetele de confirmare, fereastra este glisată cu un cadru.
    def sendData(self):
        global nRead
        global packetsLeftToSend
        global packetsLeftToReceive
        packetID = 1
        header = FRAME_DATA
        nRead = self.WinSize
        attemptsToSend = 0
        packetsLeftToSend = True
        packetsLeftToReceive = True
        while packetsLeftToReceive or packetsLeftToSend:
            if packetsLeftToSend:
                for i in range(nRead):
                    dataToSend = self.file.read(self.PackSize)
                    dataLength = len(dataToSend)
                    dataToSend = header.to_bytes(1, "big") + packetID.to_bytes(4, "big") + dataLength.to_bytes(4, "big") + dataToSend
                    self.sock.sendto(dataToSend, (self.IpReceiver, self.PortReceiver))
                    self.writeLog(f'S-a trimis pachetul cu numarul {str(packetID)}')
                    packetID += 1
            if packetsLeftToReceive:
                self.sock.settimeout(self.Timeout)
                try:
                    receivedData, addr = self.sock.recvfrom(1024)    #udp
                    if receivedData[0] == FRAME_ACKNOWLEDGE:
                        nr = int.from_bytes(receivedData[1:5], 'big')
                        self.writeLog(f'S-a receptionat ACK pentru pachetul {str(nr)}')
                        self.nrOfPacketsConf += 1
                        if receivedData[1:5] == (packetID - self.WinSize).to_bytes(4, 'big'):
                            nRead = 1
                        else:
                            self.file.seek(-self.WinSize * self.PackSize, 1)
                            packetID -= self.WinSize
                            nRead = self.WinSize
                except TimeoutError:
                    attemptsToSend += 1
                    if attemptsToSend == 10:
                        self.writeLog(f'S-a depasit numarul maxim de trimiteri! Nu poate realiza transferul!')
                        self.closeTransfer()
                        quit(-1)
                    self.file.seek(-self.WinSize * self.PackSize, 1)
                    packetID -= self.WinSize
                    packetsLeftToSend = True
                    packetsLeftToReceive = True
                    nRead = self.WinSize
            if packetID - 1 == self.nrOfPackets:
                packetsLeftToSend = False
            if self.nrOfPacketsConf == self.nrOfPackets:
                packetsLeftToReceive = False
        self.closeTransfer()

    def closeTransfer(self):
        self.file.close()
        self.log.close()
        self.sock.close()

    def writeLog(self, msg):
        self.log.write(time.strftime('%d.%m.%Y   %H:%M:%S') + ':      ' + msg + '\n')
