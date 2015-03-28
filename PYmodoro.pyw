import time
import Tkinter
import winsound

def beep(sound):
    winsound.PlaySound("%s.wav" %sound, winsound.SND_FILENAME | winsound.SND_ASYNC)

minute=60
PomodoroTime=30*minute
BreakTime=5*minute
LongBreakTime=3*BreakTime
LongBreakEvery=3

##import Skype4Py
##skype = Skype4Py.Skype()
##skype.Attach()

def SkypeOnline():
##    skype._SetCurrentUserStatus('ONLINE')
    pass
def SkypeDND():
##    skype._SetCurrentUserStatus('DND')
    pass

def ParseTime(Time):
    Minutes=Time//60
    Seconds=int(Time%60)
    String = "%02d" % (Minutes)
    String+=":"
    String+="%02d" % (Seconds)
    return String

class pomodorotimer(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent=parent
        self.initialize()
    def initialize(self):
        self.grid()

        self.TimeMeter = Tkinter.Label(self, text=ParseTime(PomodoroTime), font="Eurostile 20 bold", anchor="c",bg="lightblue")
        self.TimeMeter.grid(column=0,row=0,columnspan=2,sticky='EW')
         
        self.button=Tkinter.Button(self,text=b"START", command=self.OnButtonClick)
        self.button.grid(column=0,row=1)

        self.bind('<Return>', self.OnEnterPress)

        self.Messenger = Tkinter.Label(self, text=u"Pomodoro ready.", anchor="c")
        self.Messenger.grid(column=1,row=1,columnspan=1,sticky='EW')
        
        self.grid_columnconfigure(0,weight=1)
        self.resizable(0,0)
        self.update()
        self.geometry(self.geometry())
        
        self.iconbitmap(r'icon.ico')
        self.wm_attributes('-topmost', 1)
        self.TimerRunning = False
        self.NextUp="pomodoro"
        self.TimeRemaining=PomodoroTime
        self.TimeElapsed=0
        self.afterid=False
        self.PomodoroCounter=0
    def OnButtonClick(self):
        self.ButtonHandler()
    def OnEnterPress(self, event):
        self.ButtonHandler()
    def ButtonHandler(self):
        if self.TimerRunning:
            self.Messenger.configure(text="Cancelled.")
            SkypeOnline()
            self.after_cancel(self.afterid)
            self.afterid=False
            self.TimerRunning=False
            self.button.configure(text=b"START")
            self.TimeElapsed=0
            self.TimeMeter.configure(text=ParseTime(self.TimeRemaining-self.TimeElapsed))
        else:
            if self.NextUp=="pomodoro":
                self.Messenger.configure(text="Pomodoro running.")
                SkypeDND()
            elif self.NextUp=="break":
                self.Messenger.configure(text="Break running.")
                SkypeOnline()
            elif self.NextUp=="longbreak":
                self.Messenger.configure(text="Long break running.")
                SkypeOnline()
            self.TimerRunning=True
            self.button.configure(text=b"STOP")
            self.tick()
    def tick(self):
        if (self.TimeElapsed<self.TimeRemaining):
            self.TimeElapsed+=1
            self.TimeMeter.configure(text=ParseTime(self.TimeRemaining-self.TimeElapsed))
            self.afterid=self.after(1000,self.tick)
        else:
            self.TimerRunning=False
            self.TimeElapsed=0
            self.afterid=False
            self.button.configure(text=b"START")
            if self.NextUp=="pomodoro":
                self.PomodoroCounter+=1
                if self.PomodoroCounter%LongBreakEvery==0:
                    self.NextUp="longbreak"
                    self.TimeRemaining=LongBreakTime
                    beep("longbreak")
                else:
                    self.NextUp="break"
                    self.TimeRemaining=BreakTime
                    beep("break")
                self.Messenger.configure(text="Pomodoro done.")
                self.TimeMeter.configure(bg="lightgreen")
                SkypeOnline()
                
            elif self.NextUp=="break" or self.NextUp=="longbreak":
                self.NextUp="pomodoro"
                self.TimeRemaining=PomodoroTime
                self.Messenger.configure(text="Break done.")
                self.TimeMeter.configure(bg="lightblue")
                SkypeDND()
                beep("pomodoro")
            self.TimeMeter.configure(text=ParseTime(self.TimeRemaining-self.TimeElapsed))

            return 0
if __name__ == "__main__":
    app = pomodorotimer(None)
    app.title("PYmodoro")
    app.mainloop()
