# Alameda Hybrid Learning Constraint Solver

0) Simulcast Students are not considered as part of this
   optimization problem. They will be assigned to AM/PM cohorts as
   a second optimization problem.

1) Students will be divided into AM and PM cohorts. Siblings must
   be assigned to the same cohort.

2) Each Student has an initial Teacher assignment. Assignments MAY
   be changed, but such moves should be minimized.

3) Each classroom has a maximum capacity.

4) Each teacher has an initial Classroom assignment. We do not attempt
   to move teachers.

6) Maintaining Gender balance is desirable.

## Approach

We load the rooms, teachers, and students data. Then we group siblings
together by home address. Once siblings have been linked together, we
assign each set of siblings to an AM or PM cohort in pseudo-random
order ensuring AM and PM have roughly equal distribution. Note that we
DO NOT assign these students to a teacher in this phase.

Next, group all students based on their affinity to their current
teacher. There are 4 tiers of affinity (0-3), 0 being minimal
affinity, and 3 being maximal affinity.

For each tier, starting with maximal affinity, we shuffle the list of
students. We assign all sibling students, and then all non-sibling
students. We prefer the student's current teacher, and fall back to
other teachers within that grade level if their current teacher is
full. Non-sibling students are placed in whichever AM/PM cohort has
the least students assigned so that the AM and PM sessions remain
balanced.
