#
# IMPORTS
#

import math
import numpy as np
import random

#
# CONSTANTS
#

KINDERGARTEN = 0
FIRST_GRADE = 1
SECOND_GRADE = 2
THIRD_GRADE = 3
FOURTH_GRADE = 4
FIFTH_GRADE = 5

#
# TUNABLE PARAMETERS
#
TUNABLE_OPTIMIZATION_ITERATIONS = 2**25
TUNABLE_STUDENT_LIMIT_IMBALANCE_TOLERANCE_BY_GRADE_LEVEL = {
    KINDERGARTEN: 3,
    FIRST_GRADE: 3,
    SECOND_GRADE: 3,
    THIRD_GRADE: 3,
    FOURTH_GRADE: 3,
    FIFTH_GRADE: 3,
}
TUNABLE_ROOM_CAPACITY_EXCEEDED_SCALAR = 10
TUNABLE_ROOM_SWITCH_COST = 3

def assign_teachers_to_rooms(students, teachers, rooms):
    compute_student_limits(students, teachers)
    adjust_grade_level_student_imbalance(teachers)
    optimize_room_assignments(teachers, rooms)

def compute_student_limits(students, teachers):
    by_name = {}
    for teacher in teachers:
        by_name[teacher.name] = teacher

    for student in students:
        teacher = by_name[student.initial_teacher_name]
        teacher.initial_student_count += 1

    for teacher in teachers:
        teacher.student_limit = math.ceil(teacher.initial_student_count/2)

def adjust_grade_level_student_imbalance(teachers):
    by_grade = {}
    for teacher in teachers:
        grade_level = by_grade.setdefault(teacher.grade, [])
        grade_level.append(teacher)

    for (grade_level, grade) in by_grade.items():
        tolerance = TUNABLE_STUDENT_LIMIT_IMBALANCE_TOLERANCE_BY_GRADE_LEVEL[grade_level]
        while True:
            grade.sort(key=lambda t: t.student_limit)
            t_min = grade[0]
            t_max = grade[-1]

            if t_max.student_limit - t_min.student_limit <= tolerance:
                break

            t_max.student_limit -= 1
            t_min.student_limit += 1

ROOM_ASSIGNMENT_INVALID = 2**32 # a very large number

def teacher_room_assignment_is_valid(teacher, room):
    # TODO: maybe some room assignments are invalid
    return True


def score_teacher_room_assignment(teacher, room):
    if not teacher_room_assignment_is_valid(teacher, room):
        return ROOM_ASSIGNMENT_INVALID

    score = 0
    if teacher.student_limit > room.capacity:
        score = (teacher.student_limit - room.capacity)*TUNABLE_ROOM_CAPACITY_EXCEEDED_SCALAR
    elif teacher.student_limit < room.capacity:
        score = room.capacity - teacher.student_limit

    if teacher.initial_room_number != room.number:
        score += TUNABLE_ROOM_SWITCH_COST

    return score

def optimize_room_assignments(teachers, rooms):
    scores = np.zeros( (len(teachers), len(rooms)) )

    initial_score = 0
    initial_assignment = []
    for t in range(0, len(teachers)):
        teacher = teachers[t]
        for r in range(0, len(rooms)):
            room = rooms[r]
            score = score_teacher_room_assignment(teacher, room)
            scores[(t,r)] = score
            if room.number == teacher.initial_room_number:
                initial_score += score
                initial_assignment.append((t,r))

    # genetic algorithm, find best room assignments
    random.seed(42) # Answer to the Ultimate Question of Life, the Universe, and Everything
    best_score = initial_score
    best_assignment = initial_assignment
    n = len(best_assignment)
    for i in range(0,TUNABLE_OPTIMIZATION_ITERATIONS):
        x = random.randint(0,n-1)
        y = (x + random.randint(1,n-1)) % n

        xt, xr = best_assignment[x]
        yt, yr = best_assignment[y]
        baseline = scores[(xt,xr)] + scores[(yt,yr)]
        mutation = scores[(xt,yr)] + scores[(yt,xr)]
        if mutation < baseline:
            best_assignment[x] = (xt, yr)
            best_assignment[y] = (yt, xr)

    # Update the teachers with their room assignments, checking to
    # make sure we aren't over capacity.
    for (t, r) in best_assignment:
        teacher = teachers[t]
        room = rooms[r]
        if teacher.student_limit > room.capacity:
            raise RuntimeError("Teacher {} exceeds room {}".format(teacher.name, room.capacity))

        teacher.assigned_room = room
