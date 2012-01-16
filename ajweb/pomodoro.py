from datetime import datetime, timedelta

class Pomodoro(object):

    def __init__(self, **kwargs):
        for key in kwargs:
            if type(kwargs[key]) is not int :
                raise Exception('Please start a Pomodoro with an integer value (minutes)')
            if kwargs[key] <= 0:
                raise Exception('Please start a Pomodoro with a positive value')
            if kwargs[key] > 2147483647:
                raise Exception('The time set for the Pomodoro cannot be greater \
                than the max int32: 2147483647')
        self.__setDefaults(**kwargs)

    def __setDefaults(self, **kwargs):
        days = kwargs.get('days', 0)
        hours = kwargs.get('hours', 0)
        minutes = kwargs.get('minutes', 0)
        seconds = kwargs.get('seconds', 0)
        # if no time has been passed, set default
        if days == 0 and hours == 0 and minutes == 0 and seconds == 0:
            minutes = 25

        self.pomodoroTime = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
        self.startingTime = None
        self.active = True
        self.pauseTime = None
        self.pauses = 0

    def getTimeLeft(self):
        if self.isActive():
            if self.startingTime is None: return self.pomodoroTime
            finalTime = self.startingTime + self.pomodoroTime
            return finalTime - datetime.now()

    def start(self):
        self.startingTime = datetime.now()


    def pause(self):
        if self.isActive():
            self.pauseTime = datetime.now()
            self.pauses += 1

    def resume(self):
        if self.isActive():
            if self.pauseTime is not None:
               self.startingTime += self.pauseTime - datetime.now()


    def isActive(self):
        if self.active is False or  self.startingTime is None or \
                (self.startingTime + self.pomodoroTime) <= datetime.now():
            raise Exception('This pomodoro is no longer active')

        return True