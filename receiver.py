from random import random
from logging import *
import threading
import sys
sys.path.append('..//')


class Receiver:
    def __init__(self, IpReceiver, PortReceiver):
        self.IpReceiver = IpReceiver
        self.PortReceiver = PortReceiver
        self.Nack = 1
        self.Ack = 2
        self.Data = 4
        self.INF = 8
        form = "%(asctime)-15s-%(message)s"
        f = open("log.txt", mode="w")
        f.close()
        basicConfig(format=form, filename="log.txt", level=INFO)
        self.message = ""

    def decodeData(self, packet):
        pID = packet[1:5]
        len = packet[5:9]
        data = packet[9:]
        return pID, len, data

    def decodeINF(self, packet):
        packets = packet[1:5]
        senderPort = packet[5:7]
        fname = packet[7:]
        return packets, senderPort, fname

    def encodeAck(self, pID):
        toSend = b''
        toSend = toSend + self.Ack.to_bytes(1, "big") + pID
        return toSend

    def start(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.IpReceiver, self.PortReceiver))
            print(self.IpReceiver)
            senderPort = 0
            numberOfPackets = 0
            packetExpected = 1
            file = 0
            while True:
                msg = "Se asteapta pachetul: " + str(packetExpected)
                info(msg)
                data, addr = sock.recvfrom(2048)
                packet = bytes(data)
                print(addr)
                if packet[0] == self.INF:
                    info("S-a primit pachetul cu informatiile: \n")
                    numberOfPackets, senderPort, fileName = self.decodeINF(packet)
                    msg = "Nume fisier: " + str(fileName)+", numar de pachete " + str(int.from_bytes(numberOfPackets, "big"))
                    info(msg)
                    file = open(fileName, "wb")
                if packet[0] == self.Data:
                    packetID, length, dataF = self.decodeData(packet)
                    print(packetID)
                    if packetExpected.to_bytes(4, "big") == packetID:
                        toSend = self.encodeAck(packetID)
                        a = random()
                        if a > 0.003:
                            msg = "S-a primit pachetul cu numarul de secventa " + str(int.from_bytes(packetID, "big")) + ", lungime "+ str(int.from_bytes(length, "big"))+" octeti"
                            info(msg)
                            #s = sock.sendto(toSend, (addr[0],int.from_bytes(senderPort, "big")))
                            packetExpected += 1
                            file.write(packet[9:])
                            percent = int(int.from_bytes(packetID , "big")*100. / int.from_bytes(numberOfPackets,"big"))
                            self.interface.progressbar.config(value=percent)
                            if packetID == numberOfPackets:
                                break
                        else:
                            msg = "Nu s-a primit pachetul " + str(int.from_bytes(packetID, "big")) + "(S-a pierdut)."
                            info(msg)
            sock.close()
            file.close()
            self.interface.button.config(state="normal")
            self.interface.progressbar.config(value=0)
            self.message = "Transfer completed!!!"

        except:
            self.message = "Transfer failed!!!"
            error("Erroare la transmisie")

        finally:
            exit(-1)





