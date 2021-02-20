# Alameda Hybrid Learning Constraint Solver

0) Simulcast Students are not considered as part of this
   optimization problem. They will be assigned to AM/PM cohorts as
   a second optimization problem.

1) Students will be divided into AM and PM cohorts. Siblings must
   be assigned to the same cohort.

2) Each Student has an initial Teacher assignment. Assignments MAY
   be changed, but such moves should be minimized.

3) Each classroom has a maximum capacity.

4) Each teacher has an initial Classroom assignment. Assignments
   MAY be changed, but such moves should be minimized.

5) Teacher/Classroom assignment changes are preferable to
   Student/Teacher assignment change.

6) Maintaining Gender balance is also desirable.

7) The number of Students assigned to each Teacher should be
   approximately even across each grade level.

## Approach

Once all of the family survey data has been collected, each Teacher in
our model will be seeded with an initial student\_limit, i.e. the
ceiling(students\_opting\_in/2) for each teacher. At this point we
should address any inbalance between Teachers within each grade
level. For example, we might declare that the maximum student\_limit
difference between any two teachers within a grade level is 3. This
parameter is tunable

If Teacher A has student\_limit=7 and Teacher B has student\_limit=13,
we would adjust these to be A.student\_limit=9 and
B.student\_limit=11. This will help ensure some level of fairness among
teachers while hopefully minimizing the number of students that are
assigned to a new teacher.

Next, we will deal with room assignments. We will a score for each
(teacher, room) pair. Then we will use a genetic algorithm to find a
better set of room assignments by swapping rooms between teachers with
the goal of reducing the overall room assignment score (lower is
better). A Teacher/Room assignment will be scored based on:

1. The validity of the room assignment (assuming some teacher/room
   assignments are invalid)
2. The difference between a Room.capacity and the
   Teacher.student\_limit. A Teacher/Room assignment where a Teacher's
   student\_limit exceeds the Room Capacity is much worse than the
   Room Capacity exceeding the student_limit. Ultimately, if no
   validate set of Teacher/Room assignments exists, i.e. the solution
   with the lowest score contains Teachers assigned to Rooms where the
   student\_limit exceeds the Capacity, we may need to adjust the
   TUNABLE\_STUDENT\_LIMIT\_IMBALANCE\_TOLERANCE\_BY\_GRADE\_LEVEL.
3. Whether the Teacher must switch rooms.

Finally, we iterate through the students in pseudo-random order, and
assign them to a teacher, preferring their current teacher, and
falling back to other teachers within that grade level.


