import subprocess
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from threading import Thread
from sender import Sender


class Thread2(Thread):
    def __init__(self, apl, s):
        Thread.__init__(self)
        self.apl = apl
        self.s = s

    def run(self):
        if self.apl and self.s:
            while True:
                if self.s.nrOfPackets:
                    if self.s.nrOfPacketsConf == self.s.nrOfPackets:
                        break
                if not self.apl.thread1.is_alive():
                    exit(-1)


class App(Frame):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.thread2 = None
        self.IpSender = ''
        self.PortSender = 0
        self.IpReceiver = ''
        self.PortReceiver = 0
        self.Timeout = 0
        self.WinSize = 0
        self.PackSize = 0
        self.Failure = 0

        self.linkIpSender = StringVar()
        self.linkPortSender = StringVar()
        self.linkIpReceiver = StringVar()
        self.linkPortReceiver = StringVar()
        self.linkTimeout = StringVar()
        self.linkWinSize = IntVar()
        self.linkPackSize = StringVar()
        self.linkFailure = StringVar()

        self.listIPs = []
        self.getIPs()
        self.isConfigured = False
        self.fileName = ''
        self.interface(app)

    def interface(self, app):
        Frame.__init__(self, app)
        app.title('  Transfer de fișiere')
        app.resizable(0, 0)
        self.labelIpSender = Label(app, text='  IP Sender:')
        self.inIPSender = ttk.Combobox(app, textvariable=self.linkIpSender)
        self.inIPSender['values'] = self.listIPs
        self.labelIpSender.grid(row=1, column=0, sticky='NW')
        self.inIPSender.grid(row=1, column=1, sticky='NW')

        self.labelPortSender = Label(app, text='  Port Sender:')
        self.entryPortSender = Entry(app, textvariable=self.linkPortSender)
        self.labelPortSender.grid(row=2, column=0, sticky='NW')
        self.entryPortSender.grid(row=2, column=1, sticky='NW')

        self.labelIpReceiver = Label(app, text='  IP Receiver:')
        self.entryIpReceiver = Entry(app, textvariable=self.linkIpReceiver)
        self.labelIpReceiver.grid(row=3, column=0, sticky='NW')
        self.entryIpReceiver.grid(row=3, column=1, sticky='NW')

        self.labelPortReceiver = Label(app, text='  Port Receiver:')
        self.entryPortReceiver = Entry(app, textvariable=self.linkPortReceiver)
        self.labelPortReceiver.grid(row=4, column=0, sticky='NW')
        self.entryPortReceiver.grid(row=4, column=1, sticky='NW')

        self.labelTimeout = Label(app, text='  Timeout(ms):')
        self.entryTimeout = Entry(app, textvariable=self.linkTimeout)
        self.labelTimeout.grid(row=5, column=0, sticky='NW')
        self.entryTimeout.grid(row=5, column=1, sticky='NW')
        self.entryTimeout.insert('end', '1000')

        self.labelWinSize = Label(app, text='  Dimensiunea ferestrei glisante:')
        self.labelWinSize.grid(row=6, column=0, rowspan=6, sticky='NW')
        self.scaleWinSize = Scale(app, orient=HORIZONTAL, length=250, from_=1, to=100, resolution=1,
                                  troughcolor='#cce6ff', variable=self.linkWinSize)
        self.scaleWinSize.grid(row=7, column=0, columnspan=2, sticky='N')

        self.labelPackSize = Label(app, text='  Dimensiunea pachetului:')
        self.labelPackSize.grid(row=9, column=0, rowspan=6, sticky='NW')
        self.entryPackSize = Entry(app, textvariable=self.linkPackSize)
        self.entryPackSize.grid(row=9, column=1, sticky='NE')
        self.entryPackSize.insert('end', '10')

        self.labelFailure = Label(app, text='  Șansa de a pierde un pachet:')
        self.entryFailure = Entry(app, textvariable=self.linkFailure)
        self.labelFailure.grid(row=11, column=0, rowspan=6, sticky='NW')
        self.entryFailure.grid(row=11, column=1, sticky='NW')
        self.entryFailure.insert('end', '0.1')

        self.buttonConfiguration = Button(text='Configurare', command=self.validateInput, bg='#80bfff')
        self.buttonConfiguration.grid(row=12, column=0, columnspan=2, pady=10, sticky='N')

        self.buttonOpenFile = Button(text='Deschidere fișier', command=self.selectFile, bg='#80bfff')
        self.buttonOpenFile.grid(row=23, column=0, columnspan=2, sticky='N')

        self.labelSenderView = Label(app, text='View Sender')
        self.entrySenderView = Text(app, state=DISABLED, height=15, wrap=WORD)
        self.scrollbarSenderView = Scrollbar(app, command=self.entrySenderView.yview)
        self.entrySenderView.config(yscrollcommand=self.scrollbarSenderView.set)
        self.labelSenderView.grid(row=0, column=2, columnspan=2, sticky='N')
        self.entrySenderView.grid(row=1, column=2, rowspan=6, columnspan=2, padx=10, sticky='N')
        self.scrollbarSenderView.grid(row=1, column=3, ipady=97, rowspan=6, sticky='NE')

        self.labelReceiverView = Label(app, text='View Receiver')
        self.entryReceiverView = Text(app, state=DISABLED, height=15, wrap=WORD)
        self.scrollbarReceiverView = Scrollbar(app, command=self.entryReceiverView.yview)
        self.entryReceiverView.config(yscrollcommand=self.scrollbarReceiverView.set)
        self.labelReceiverView.grid(row=8, column=2, columnspan=2, sticky='N')
        self.entryReceiverView.grid(row=9, column=2, rowspan=15, columnspan=2, padx=10, sticky='N')
        self.scrollbarReceiverView.grid(row=9, column=3, ipady=97, rowspan=15, sticky='NE')

        self.buttonStart = Button(app, text='START', bg='#99ff99', command=self.createSendThread)
        self.buttonStart.grid(row=25, column=2, pady=10)
        self.buttonStart['state'] = 'disabled'

        self.buttonStop = Button(app, text='STOP', bg='#ff3300')
        self.buttonStop.grid(row=25, column=3, pady=10)
        self.buttonStop['state'] = 'disabled'

    def insertViewSender(self, text):
        self.entrySenderView.configure(state='normal')
        self.entrySenderView.insert('end', text)
        self.entrySenderView.configure(state='disabled')
        self.entrySenderView.see('end')

    def insertViewReceiver(self, text):
        self.entryReceiverView.configure(state='normal')
        self.entryReceiverView.insert('end', text)
        self.entryReceiverView.configure(state='disabled')
        self.entryReceiverView.see('end')

    def validateInput(self):
        config = True
        if self.validateIP(self.linkIpSender.get()):
            self.IpSender = self.linkIpSender.get()
        else:
            config = False
            self.insertViewSender('IP sender -> invalid \n')
        if self.validatePort(self.linkPortSender.get()):
            self.PortSender = self.linkPortSender.get()
        else:
            config = False
            self.insertViewSender('PORT sender -> invalid \n')
        if self.validateIP(self.linkIpReceiver.get()):
            self.IpReceiver = self.linkIpReceiver.get()
        else:
            config = False
            self.insertViewReceiver('IP  receptor -> invalid \n')
        if self.validatePort(self.linkPortReceiver.get()):
            self.PortReceiver = self.linkPortReceiver.get()
        else:
            config = False
            self.insertViewReceiver('PORT receptor -> invalid \n')

        if config:
            self.insertViewSender('\tSTATUS -> CONFIGURAT! \n')
            self.isConfigured = True
            self.buttonStart['state'] = 'active'
        else:
            self.insertViewSender('\tSTATUS -> NECONFIGURAT! \n')
            self.buttonStart['state'] = 'disabled'

    @staticmethod
    def validateIP(IP):
        for i in range(len(IP)):
            if IP[i] not in '.0123456789':
                return False
        if IP.count('.') != 3:
            return False
        for nr in IP.split('.'):
            if int(nr) < 0 or int(nr) > 255:
                return False
        return True

    @staticmethod
    def validatePort(PORT):
        if not PORT.isdigit() or int(PORT) < 0 or int(PORT) > 65535:
            return False
        else:
            return True

    def selectFile(self):
        self.fileName = filedialog.askopenfilename()
        self.insertViewSender('Fișierul ' + self.fileName + ' a fost selectat!')

    def getIPs(self):
        for line in str(subprocess.check_output('ipconfig'), 'ISO-8859-1').splitlines():
            if line.find('IPv4 Address') != -1:
                index = line.find(':')
                self.listIPs.append(line[index + 2:])

    def createSendThread(self):
        if self.isConfigured and self.fileName:
            self.buttonStart["state"] = "disabled"
            self.thread1 = Thread(target=self.sendFile, args=())
            self.thread1.start()
        else:
            print("aplicatia nu este configurata")

    def sendFile(self):

        s = Sender(self.IpSender, self.PortSender, self.IpReceiver, self.PortReceiver, self.Timeout, self.WinSize,
                   self.PackSize, self.Failure, self.fileName)

        self.thread2 = Thread2(self, s)
        self.thread2.start()
        s.readFile()
        s.sendInfo()
        s.sendData()
