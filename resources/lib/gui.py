import os
import sys
import xbmc
import xbmcgui
from datetime import datetime
import locale


__addon__ = sys.modules["__main__"].__addon__
__addonid__ = sys.modules["__main__"].__addonid__
__cwd__ = sys.modules["__main__"].__cwd__

loc = locale.getlocale(locale.LC_ALL) # get current locale
locale.setlocale(locale.LC_ALL, '')

def log(txt):
    if isinstance(txt, str):
        txt = txt.decode("utf-8")
    message = u'%s: %s' % (__addonid__, txt)
    xbmc.log(msg=message.encode("utf-8"), level=xbmc.LOGDEBUG)


class Screensaver(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        self.stop = False
        self.Monitor = MyMonitor(action=self.exit)

    def onInit(self):
        self.group_qclock = self.getControl(30098)
        self.group_info = self.getControl(30099)
        self.switchtime = 0
        self.displayleft = False
        self.time_control = self.getControl(30100)
        self.colon_control = self.getControl(30101)
        self.weekday_control = self.getControl(30102)
        self.date_control = self.getControl(30103)
        self.weathericon_control = self.getControl(30104)
        while (not xbmc.abortRequested) and (not self.stop):
            self.displayTime()
            xbmc.sleep(1000)

    def exit(self):
        self.stop = True
        self.close()

    def displayTime(self):
        now = datetime.now()
        hours = now.strftime("%H")
        mins = now.strftime("%M")
        date = now.strftime("%d.%m.%Y")
        weekday = now.strftime("%A")
        self.time_control.setLabel(hours + "  " + mins)
        if now.second%2==0:
            self.colon_control.setVisible(True)
        else:
            self.colon_control.setVisible(False)
        self.date_control.setLabel(date)
        self.weekday_control.setLabel(weekday)
        self.weathericon_control.setImage(os.path.join(__cwd__,"resources/weathericons/","set5",xbmc.getInfoLabel('Window(Weather).Property(Current.FanartCode)')) + ".png")
        if self.switchtime == 300:
            self.switchtime = 0
            if self.displayleft:
                self.displayleft = False
                self.group_qclock.setPosition(100, 88)
                self.group_info.setPosition(800, 88)
            else:
                self.displayleft = True
                self.group_qclock.setPosition(600, 88)
                self.group_info.setPosition(100, 88)
        self.switchtime = self.switchtime + 1
    
class MyMonitor(xbmc.Monitor):

    def __init__(self, *args, **kwargs):
        self.action = kwargs['action']

    def onScreensaverDeactivated(self):
        self.action()
