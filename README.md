# safari-dinner

Safari dinner organization wizard
=================================

* course1 = Starter (swedish: förrätt)
* course2 = Main (swedish: huvudrätt)
* course3 = Dessert (swedish: efterrätt)
* course4 = Nightfood (swedish: nattamat)

Each participant consists of two persons (normally a couple) and is host for one course.

At each course there are four participants: the host and three guests.
* at course1 one guest is host for course2, one guest is host for course3 and one guest is host for course4.
* at course2 one guest is host for course1, one guest is host for course3 and one guest is host for course4.
* at course3 one guest is host for course1, one guest is host for course2 and one guest is host for course4.
* at course4 one guest is host for course1, one guest is host for course2 and one guest is host for course3.

Course1-3 take place in the host's house. Course4 is a common gathering place where all participants meet
and the hosts provide a buffet for everybody. But to guarantee that food requirements are met (allergies, vegetarian etc)
there is still guests for each host for course4.

The participants living far from the center shall be hosts for course4. If they are less than one fourth some participants from the
center shall also be hosts for course4.

Participants register by a form at https://docs.google.com/forms/. They shall provide this information:
* familyName
* name
* address
* email
* phone
* preferredCourse
* specialFoodPerson1
* specialFoodPerson2

The organizer combines hosts and guests for the courses such that any two participants are at the same course at most once, and all
guests are hosts for different courses.

The organizer sends **email1** to each particant specifying start time and place (**meetingPoint1**),
which course it shall host and specialFood requirements (if any) for its guests.

The safari dinner starts at **meetingPoint1**. Drinks are served by the organizer. The participants not
being host for course1 get **letter1** specifying the address where they shall have course1. The organizer tells
everyone where to meet after course1 (**meetingPoint2**) and where to meet for course4 (**meetingPoint3**).

All participants go to course1 and when it is finished everybody goes to **meetingPoint2**.

At **meetingPoint2** drinks are served by the organizer. Each participant not being host for course2 get **letter2**
specifying where to go for course2. The participant being host for course2 get **letter3**.

All participants go to course2 and when it is finished the hosts opens **letter3** containing **letter3.1**, **letter3.2**, **letter3.3**. They are for the participants at course2 who are not host for course3. They specify where they shall have course3.

All participants go to course3 and when it is finished everybody goes to **meetingPoint3**.

At **meetingPoint3** there is music and dance. Later the hosts for course4 provide Nightfood for everybody (like a buffet).

GRAPHICALLY (time is downwards)
===============================

```
receive email1
   |
  ...
   |
meetingPoint1 (receive letter1)
   \
    \
   course1
      \
       \
    meetingPoint2 (receive letter2 if not host for course2, else receive letter3)
        \
         \
       course2 (receive letter3.1, letter3.2, letter3.3)
           \
            \
          course3
              \
               \
            meetingPoint3-course4
```

Special considerations
======================

Requirements to make the algorithm work
---------------------------------------
1. the number of participants shall be a multiple of 4
2. the least number of participants must be TBD
3. the number of participants living far from the center shall not be greater than 1/4 of the total number of participants

Workarounds if the requirements are not met
-------------------------------------------
1. not met: introduce dummy participants in the list and have empty seats
2. not met: ask more persons to join
3. not met: TBD

