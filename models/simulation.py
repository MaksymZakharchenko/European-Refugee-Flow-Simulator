def simulate(population, affected_percent):
    affected_people = population * affected_percent / 100
    displaced_people = affected_people * 0.4
    return displaced_people