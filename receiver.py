from random import random
from logging import *
import socket


class Receiver:
    def __init__(self, IpReceiver, PortReceiver, Failure):
        self.IpReceiver = IpReceiver
        self.PortReceiver = PortReceiver
        self.Failure = Failure
        self.Nack = 1
        self.Ack = 2
        self.Data = 4
        self.INF = 8
        form = "%(asctime)-15s-%(message)s"
        f = open("log.txt", mode="w")
        f.close()
        basicConfig(format=form, filename="log.txt", level=INFO)
        self.message = ""

    @staticmethod
    def decodeData(packet):
        packetID = packet[1:5]
        length = packet[5:9]
        data = packet[9:]
        return packetID, length, data

    @staticmethod
    def decodeINF(packet):
        packets = packet[1:5]
        senderPort = packet[5:7]
        fileName = packet[7:]
        return packets, senderPort, fileName

    def encodeAck(self, packetID):
        toSend = b''
        toSend = toSend + self.Ack.to_bytes(1, "big") + packetID
        return toSend

    def start(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.IpReceiver, self.PortReceiver))
            senderPort = 0
            numberOfPackets = 0
            packetExpected = 1
            file = 0
            while True:
                msg = f"Se asteapta pachetul: {str(packetExpected)}"
                info(msg)
                data, addr = sock.recvfrom(2048)
                packet = bytes(data)
                if packet[0] == self.INF:
                    info("S-a primit pachetul cu informatiile: \n")
                    numberOfPackets, senderPort, fileName = self.decodeINF(packet)
                    msg = f"Nume fisier: {str(fileName)}, numar de pachete: {str(int.from_bytes(numberOfPackets, 'big'))}"
                    info(msg)
                    file = open(fileName, "wb")
                if packet[0] == self.Data:
                    packetID, length, dataF = self.decodeData(packet)
                    if packetExpected.to_bytes(4, "big") == packetID:
                        toSend = self.encodeAck(packetID)
                        if random() > (self.Failure / 100):
                            msg = f"S-a primit pachetul cu numarul de secventa: {str(int.from_bytes(packetID, 'big'))}, " \
                                  f"lungime: {str(int.from_bytes(length, 'big'))} octeti"
                            info(msg)
                            sock.sendto(toSend, (addr[0], int.from_bytes(senderPort, "big")))
                            packetExpected += 1
                            file.write(packet[9:])
                            if packetID == numberOfPackets:
                                break
                        else:
                            msg = f"Nu s-a primit pachetul {str(int.from_bytes(packetID, 'big'))}! S-a pierdut!"
                            info(msg)
            sock.close()
            file.close()
            self.message = "Transferul s-a realizat cu succes!"
        except:
            self.message = "Transferul nu s-a realizat!"
            error("Eroare la transmisie!")
        finally:
            exit(-1)
