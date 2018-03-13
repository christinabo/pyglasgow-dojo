from datetime import date
import unittest
from rota import makeRota
import pandas as pd

class RotaTest(unittest.TestCase):
    def setUp(self):
        self.taskSchedule = {
            date(2017, 10, 25): {'Driving': '', 'Shopping': ''},
            date(2017, 10, 26): {'Cleaning': '', 'Cooking': '', 'Shopping': ''},
            date(2017, 10, 27): {'Cleaning': '', 'Cooking': ''},
            date(2017, 10, 28): {'Cleaning': '', 'Cooking': '', 'Shopping': ''},
            date(2017, 10, 29): {'Cleaning': '', 'Cooking': ''},
            date(2017, 10, 30): {'Driving': 'Roger'},
            date(2017, 10, 31): {'Driving': 'Roger'},
        }
        self.skillMatrix = {'Cleaning': {},
                            'Cooking': {'Gordon': False, 'Roger': False},
                            'Driving': {'Yuri': False},
                            'Shopping': {}}
        self.vacationSchedule = {
            date(2017, 10, 25): {},
            date(2017, 10, 26): {'Gordon': True, 'Roger': True},
            date(2017, 10, 27): {'Yuri': True},
            date(2017, 10, 28): {'Erfan': True},
            date(2017, 10, 29): {'Gordon': True, 'Yuri': True},
            date(2017, 10, 30): {},
            date(2017, 10, 31): {},
        }

    def testAllTasksHaveAnAssignee(self):
        rota = makeRota(self.taskSchedule, self.skillMatrix, self.vacationSchedule)

        for day in rota:
            for task in rota[day]:
                if self.taskSchedule[day].get(task, None) is not None:
                    self.assertTrue(rota[day][task])

    def testPersonOnVacationNotOnRota(self):
        rota = makeRota(self.taskSchedule, self.skillMatrix, self.vacationSchedule)

        for day in rota:
            for task in rota[day]:
                self.assertNotIn(rota[day][task], self.vacationSchedule[day])

    def testOnlySkilledAssignees(self):
        rota = makeRota(self.taskSchedule, self.skillMatrix, self.vacationSchedule)
        for day in rota:
            for task in rota[day]:
                self.assertNotIn(rota[day][task], self.skillMatrix[task])

    def testVolunteersAreAssignedCorrectly(self):
        rota = makeRota(self.taskSchedule, self.skillMatrix, self.vacationSchedule)
        print(rota)
        for day in rota:
            for task in rota[day]:
                if self.taskSchedule[day].get(task, None):
                    self.assertEqual(self.taskSchedule[day][task], rota[day][task])

    def testTasksAreAssignedFairly(self):
        rota = makeRota(self.taskSchedule, self.skillMatrix, self.vacationSchedule)
        df = pd.DataFrame(rota)
        print(df)
        tasksByPerson = {}
        for day in rota:
            for task in rota[day]:
                tasksByPerson[rota[day][task]] = tasksByPerson.get(rota[day][task], 0) + 1

        avg = sum([len(self.taskSchedule[tasksForDay]) for tasksForDay in self.taskSchedule]) / len(tasksByPerson)

        for person in tasksByPerson:
            self.assertLessEqual(abs(avg - tasksByPerson[person]), 1)


