from tkinter import *


class App(Frame):
    def __init__(self, app, **kw):
        super().__init__(**kw)
        self.IpSender = ''
        self.PortSender = 0
        self.IpReceiver = ''
        self.PortReceiver = 0
        self.Timeout = 0
        self.WinSize = 0
        self.Failure = 0

        self.linkIpSender = StringVar()
        self.linkPortSender = StringVar()
        self.linkIpReceiver = StringVar()
        self.linkPortReceiver = StringVar()
        self.linkTimeout = StringVar()
        self.linkWinSize = StringVar()
        self.linkFailure = StringVar()

        self.interface(app)

    def interface(self, app):
        Frame.__init__(self, app)
        app.title("Transfer de fișiere")
        app.resizable(0, 0)
        self.labelIpSender = Label(app, text="IP Sender:")
        self.entryIpSender = Entry(app)
        self.labelIpSender.grid(row=1, column=0, sticky='NW')
        self.entryIpSender.grid(row=1, column=1, sticky='NW')

        self.labelPortSender = Label(app, text="Port:")
        self.entryPortSender = Entry(app)
        self.labelPortSender.grid(row=2, column=0, sticky='NW')
        self.entryPortSender.grid(row=2, column=1, sticky='NW')

        self.labelIpReceiver = Label(app, text="IP Receiver:")
        self.entryIpReceiver = Entry(app)
        self.labelIpReceiver.grid(row=3, column=0, sticky='NW')
        self.entryIpReceiver.grid(row=3, column=1, sticky='NW')

        self.labelPortReceiver = Label(app, text="Port:")
        self.entryPortReceiver = Entry(app)
        self.labelPortReceiver.grid(row=4, column=0, sticky='NW')
        self.entryPortReceiver.grid(row=4, column=1, sticky='NW')

        self.labelTimeout = Label(app, text="Timeout(ms):")
        self.entryTimeout = Entry(app)
        self.labelTimeout.grid(row=5, column=0, sticky='NW')
        self.entryTimeout.grid(row=5, column=1, sticky='NW')
        self.entryTimeout.insert('end', "1000")

        self.labelWinSize = Label(app, text="Dimensiunea ferestrei glisante:")
        self.labelWinSize.grid(row=6, column=0, rowspan=6, sticky='NW')
        self.scaleWinSize = Scale(app, orient=HORIZONTAL, length=250, from_=1, to=100, resolution=1, troughcolor='#cce6ff')
        self.scaleWinSize.grid(row=7, column=0, columnspan=2, sticky='N')

        self.labelPackSize = Label(app, text="Dimensiunea pachetului:")
        self.labelPackSize.grid(row=9, column=0, rowspan=6, sticky='NW')
        self.entryPackSize = Entry(app)
        self.entryPackSize.grid(row=9, column=1, sticky='NE')

        self.labelFailure = Label(app, text="Șansa de a pierde un pachet:")
        self.entryFailure = Entry(app)
        self.labelFailure.grid(row=11, column=0, rowspan=6, sticky='NW')
        self.entryFailure.grid(row=11, column=1, sticky='NW')
        self.entryFailure.insert('end', "0.1")

        self.buttonConfiguration = Button(text='Configurare', bg='#80bfff')
        self.buttonConfiguration.grid(row=12, column=0, columnspan=2, pady=10, sticky='N')

        self.buttonOpenFile = Button(text='Deschidere fișier', bg='#80bfff')
        self.buttonOpenFile.grid(row=23, column=0, columnspan=2, sticky='N')

        self.labelSenderView = Label(app, text="View Sender")
        self.entrySenderView = Text(app, state=DISABLED, height=15, wrap=WORD)
        self.scrollbarSenderView = Scrollbar(app, command=self.entrySenderView.yview)
        self.entrySenderView.config(yscrollcommand=self.scrollbarSenderView.set)
        self.labelSenderView.grid(row=0, column=2, columnspan=2, sticky='N')
        self.entrySenderView.grid(row=1, column=2, rowspan=6, columnspan=2, padx=10, sticky='N')
        self.scrollbarSenderView.grid(row=1, column=3, ipady=97, rowspan=6, sticky='NE')

        self.labelReceiverView = Label(app, text="View Receiver")
        self.entryReceiverView = Text(app, state=DISABLED, height=15, wrap=WORD)
        self.scrollbarReceiverView = Scrollbar(app, command=self.entryReceiverView.yview)
        self.entryReceiverView.config(yscrollcommand=self.scrollbarReceiverView.set)
        self.labelReceiverView.grid(row=8, column=2, columnspan=2, sticky='N')
        self.entryReceiverView.grid(row=9, column=2, rowspan=15, columnspan=2, padx=10, sticky='N')
        self.scrollbarReceiverView.grid(row=9, column=3, ipady=97, rowspan=15, sticky='NE')

        self.buttonStart = Button(app, text="START", bg='#99ff99')
        self.buttonStart.grid(row=25, column=2, pady=10)

        self.buttonStop = Button(app, text="STOP", bg='#ff3300')
        self.buttonStop.grid(row=25, column=3, pady=10)

    def validateInput(self):
        config = False
