import math
import random

generators = 200
breakdown_cost = 75
wage = 30
la = 1 / 400
hours = 10000


def repaired_generators(repair_people):
    g = 0
    for _ in range(repair_people):
        r = random.random()
        if r >= 0.80:
            g += 2
        elif r >= 0.28:
            g += 1
    return g


def breakdown(n, time):
    cnt = 0
    time = 1
    for _ in range(n):
        if random.random() >= math.exp(-la * time):
            cnt += 1
    return cnt


def simulate(work_info, repair_people):
    work_generators = work_info[0]
    time = work_info[1] + 1

    # for D
    onsite = work_info[2]
    if onsite < 0:
        onsite += 1
    if onsite == 0:
        if work_generators  <= generators - 2:
            onsite += 1
            repair_people += 1
    else:
        repair_people += 1
        onsite += 1
        if onsite == 4:
            onsite = -2   

    breakdown_cnt = breakdown(work_generators, time)
    cnt = repaired_generators(repair_people)
    # cnt = 1     # for C
    work_info[0] = min(generators, work_generators + cnt) - breakdown_cnt
    if breakdown_cnt == 0:
        work_info[1] += 1
    # else:
    #     work_info[1] = 0
    elif breakdown_cnt == 1:
        work_info[1] = 0
    else:
        work_info[1] -= 2
    work_info[2] = onsite

    return wage * repair_people + (generators - work_generators) * breakdown_cost


if __name__ == "__main__":
    # info = [generators, 0]
    info = [generators, 0, 0]   # for D
    repair_people = 1
    # repair_people = 2   # for B
    cost = 0
    for t in range(hours):
        cost += simulate(info, repair_people)

    print(cost / hours)
