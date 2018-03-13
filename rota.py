def makeRota(taskSchedule, skillMatrix, vacationSchedule):
    people = {'Gordon': 0, 'Erfan': 0, 'Roger': 0, 'Yuri': 0}
    rota = {}

    for day in taskSchedule:
        rota[day] = {}
        for task in taskSchedule[day]:
            if taskSchedule[day][task]:
                rota[day][task] = taskSchedule[day][task]
                people[taskSchedule[day][task]] = people[taskSchedule[day][task]] + 1
            else:
                avg = sum(people.values())/len(people)
                available = [person for person in people
                             if person not in vacationSchedule[day] and skillMatrix[task].get(person, True)]
                person = next( ( p for p in available if people[p] == min([people[person] for person in available]) ) )
                rota[day][task] = person
                people[person] = people[person] + 1
    return rota
