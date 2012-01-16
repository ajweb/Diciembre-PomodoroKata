import unittest
from datetime import timedelta
import time
from pomodoro import Pomodoro

class PomodoroTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreatePomodoros(self):
        pomo = Pomodoro()
        self.assertEquals( timedelta(minutes=25), pomo.pomodoroTime,
            'A pomodoro starts with a default time of 25 minutes and it \
            does not start counting down until it is started')

        pomo2 = Pomodoro(minutes=1)
        self.assertEquals( timedelta(minutes=1), pomo2.pomodoroTime,
            'A pomodoro can be started with any integer positive value')
        self.assertTrue( pomo2.pomodoroTime == timedelta(minutes=1),
            'A pomodoro can be created with the low boundary value' )

        # max int32 value
        pomo3 = Pomodoro(minutes=2147483647)
        self.assertEqual( timedelta(minutes=2147483647), pomo3.pomodoroTime,
            'A pomodoro can be created with the high boundary value')
        # test that we can't create pomodoros with non valid values
        self.assertRaises( Exception, Pomodoro, -2)
        self.assertRaises( Exception, Pomodoro, 0)
        self.assertRaises( Exception, Pomodoro, 'a string' )
        self.assertRaises( Exception, Pomodoro, [] )

    def testStartAndRestartPomodoros(self):
        pomo = Pomodoro()
        pomo.start()
        self.assertTrue( pomo.getTimeLeft() < timedelta(minutes=25), 'A started pomodoro initiates the countdown' )
        pomo.start()
        self.assertTrue( pomo.getTimeLeft().seconds/60 == 24 )


    def testPauseAndResumePomodoros(self):
        pomo = Pomodoro()
        # we cannot pause a Pomodoro that has not been started yet
        self.assertRaises( Exception, pomo.pause )
        pomo.start()
        time1 = pomo.getTimeLeft()
        pomo.pause()
        time.sleep(1)
        pomo.resume()
        time2 = pomo.getTimeLeft()
        self.assertTrue( time2 + timedelta(seconds=1) < time1  )

    def testPomodoroNotActiveAfterItsTimePassed(self):
        pomo = Pomodoro(seconds=1)
        pomo.start()
        time.sleep(1)
        self.assertRaises( Exception, pomo.pause )

    def testPomodoroPausesCounter(self):
        pomo = Pomodoro()
        pomo.start()
        self.assertEquals( pomo.pauses, 0 )
        pomo.pause()
        pomo.resume()
        self.assertEquals( pomo.pauses, 1 )
        i=0
        while i<10:
            pomo.pause()
            pomo.resume()
            i += 1
        self.assertEquals( pomo.pauses, 11 )

