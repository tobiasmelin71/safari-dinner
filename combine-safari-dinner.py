#!/usr/bin/env python
# -*- coding: utf-8 -*-
# run me with e.g.: rm -rf out; python combine-safari-dinner.py -o out -f testInputData/all.csv
# tested on Ubuntu 16.04

import argparse
import logging
import os
import random
import re
import sys

# debug configuration
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

# init random generator
random.seed()

# Parse command line arguments
argparser = argparse.ArgumentParser(description="Assigns meals, combines hosts and guests, and generates letters for a safari dinner.")
argparser.add_argument("-o", "--out-dir",
                        required = True,
                        dest = "outDir",
                        help = "Directory that will be created. It will contain all generated files.")
argparser.add_argument("-f", "--file",
                        required = True,
                        dest = "csvFile",
                        help = "Csv file with information the participants entered when they submitted the Google party invite form.")
#TODO add optional argument to set the debug level
args = argparser.parse_args()
try:
    os.mkdir(args.outDir)
    logging.info("Out directory %s was created." % args.outDir)
except OSError as e:
    logging.error("Failed to create directory %s. Error = %s." % (args.outDir, e.strerror))
    sys.exit(-1)
if not os.path.isfile(args.csvFile):
   print "Fatal error: file", args.csvFile, "does not exist"
   sys.exit(1)


# Class for participant. A participant is one couple (i.e. two persons) that has signed up for the safari dinner
class Participant(object):
    def __init__(self, familyName, name, address, email, phone, preferredCourse, specialFoodPerson1, specialFoodPerson2):
        self.id = 0 # id is assigned later
        self.familyName = familyName
        self.name = name
        self.address = address
        self.email = email 
        self.phone = phone 
        self.preferredCourse = preferredCourse
        self.specialFoodPerson1 = specialFoodPerson1
        self.specialFoodPerson2 = specialFoodPerson2
        self.course = None # the course this participant is host for, will be assigned later
        self.guests = [] # will later be filled with 3 id:s

    def getFamilyName(self):
        return self.familyName

    def getName(self):
        return self.name

    def getAddress(self):
        return self.address

    def getEmail(self):
        return self.email

    def getpreferredCourse(self):
        return self.preferredCourse

    def hasCourse(self): 
        return False if self.course is not None else True

    def isHostFor(self, course): 
        return True if self.course is course else False

    def setCourse(self, course):
        self.course = course

    def getCourse(self):
        return self.course

    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def addGuest(self, guest):
        self.guests.append(guest)

    def getGuests(self):
        return self.guests

    def getSpecialFoodPerson1(self):
        return self.specialFoodPerson1

    def getSpecialFoodPerson2(self):
        return self.specialFoodPerson2

    def dump(self):
        print "============================="
        print "id =", self.id
        print "familyName =", self.familyName
        print "name =", self.name
        print "address =", self.address
        print "email =", self.email
        print "phone =", self.phone
        print "preferredCourse =", self.preferredCourse
        print "specialFoodPerson1 =", self.specialFoodPerson1
        print "specialFoodPerson2 =", self.specialFoodPerson2
        print "course =", self.course
        print "guests =", self.guests


# Read the csv file downloaded from the Google form and put the info in a list array of objects
csvDelimiter = '","'
participants = []
with open(args.csvFile) as f:
   for line in f:
      if line.startswith('"Timestamp'):
         continue # skip csv header
      next = Participant(line.split(csvDelimiter)[1], 
                         line.split(csvDelimiter)[2],
                         line.split(csvDelimiter)[3],
                         line.split(csvDelimiter)[4],
                         line.split(csvDelimiter)[5],
                         line.split(csvDelimiter)[6].decode('utf-8'),
                         line.split(csvDelimiter)[7],
                         line.split(csvDelimiter)[8][:-3]) # :-3 deletes last 3 chars (quotation, line feed, carriage return)
      participants.append(next);
f.close()
nbrOfParticipants = len(participants)
oneFourth = nbrOfParticipants/4
logging.info("Number of participants = %s", nbrOfParticipants)
logging.info("DONE with: Read the csv file downloaded from the Google form and put the info in a list array of objects")
assert nbrOfParticipants <= 400, "Number of participants cannot be larger than 400 due to implementation of id numbers"
assert (oneFourth)*4 == nbrOfParticipants, "Number of participants is not a multiple of 4"
#TODO need to assert that the strings name + familyName is unique, else letter files will be overwritten


# Determine which course each participant shall be host for
COURSE_STARTER = "förrätt"
COURSE_MAIN = "huvudrätt"
COURSE_DESSERT = "efterrätt"
COURSE_NIGHT = "nattamat"
courses = [COURSE_STARTER, COURSE_MAIN, COURSE_DESSERT, COURSE_NIGHT]
MUST_HAVE_TEXT = "ste ha nattamat" # Måste ha nattamat (bor utanför Harlösa), but regexp problem with åäö
DONT_CARE_TEXT = "Inget " # Inget önskemål, but regexp problem with åäö
WANT_TEXT_INGRESS = "Vill ha "
NOT_WANT_TEXT_INGRESS = "Vill inte ha "
coursesToAssign = []
for n in range(0, oneFourth):
    coursesToAssign.extend(courses)
random.shuffle(coursesToAssign)
# workaround to print list with strings having åäö. If printing separate item the workaround is not needed
logging.info("coursesToAssign shuffled = %s", repr(coursesToAssign).decode("unicode-escape").encode('latin-1'))

# Handle participants that must be host for nightfood
course = "nattamat"
for p in participants:
    pattern = re.compile(MUST_HAVE_TEXT) 
    if pattern.search(p.getpreferredCourse()):
        logging.info("Match: \"%s\" for participant %s, %s" % (MUST_HAVE_TEXT, p.getFamilyName(), p.getName()))
        if course in coursesToAssign:
            p.setCourse(course)
            logging.info("setCourse: %s" % course)
            coursesToAssign.remove(course) # removes one (the first) occurrence and that is what we want
        else:
            logging.error("Too many participants must be host for %s. Fatal error, exiting." % course)
            sys.exit(-1)

# Handle participants that wants to be host for a specific course
for course in courses:
    for p in participants:
       pattern = re.compile(WANT_TEXT_INGRESS + course[0]) # only first character to get rid of regexp problem with åäö
       if pattern.search(p.getpreferredCourse()):
           logging.info("Match: \"%s\" for participant %s, %s" % (WANT_TEXT_INGRESS + course, p.getFamilyName(), p.getName()))
           if course in coursesToAssign:
               p.setCourse(course)
               logging.info("setCourse: %s" % course)
               coursesToAssign.remove(course) # removes one (the first) occurrence and that is what we want
           else:
              logging.error("Too many participants want to be host for %s." % course)
              sys.exit(-1)       

# Handle participants that do not want to be host for a specific course
for course in courses:
    for p in participants:
       pattern = re.compile(NOT_WANT_TEXT_INGRESS + course[0]) # only first character to get rid of regexp problem with åäö
       if pattern.search(p.getpreferredCourse()):
           logging.info("Match: \"%s\" for participant %s, %s" % (NOT_WANT_TEXT_INGRESS + course, p.getFamilyName(), p.getName()))
           coursesOthers = list(courses)
           coursesOthers.remove(course)
           random.shuffle(coursesOthers) 
           found = False
           for potentialCourse in coursesToAssign:
              if potentialCourse in coursesOthers:
                  found = True
                  p.setCourse(potentialCourse)
                  logging.info("setCourse: %s" % potentialCourse)
                  coursesToAssign.remove(potentialCourse) # removes one (the first) occurrence and that is what we want
                  break
           if not found:
              logging.error("\"%s\": setCourse impossible" % (NOT_WANT_TEXT_INGRESS + course, course))
              print "Remaining courses to assign:", coursesToAssign
              sys.exit(-1)  

# Handle participants that do not have any preference on which course to be host for
for p in participants:
    pattern = re.compile(DONT_CARE_TEXT)
    if pattern.search(p.getpreferredCourse()):
        logging.info("Match: \"%s\" for participant %s, %s" % (DONT_CARE_TEXT, p.getFamilyName(), p.getName()))
        courseToSet = coursesToAssign.pop() # pop returns the last item and removes it from the list
        p.setCourse(courseToSet) 
        logging.info("setCourse: %s" % courseToSet)
assert len(coursesToAssign) == 0, "Not all items in coursesToAssign where assigned to the participants"
logging.info("DONE with: Determine which course each participant shall be host for")


# Assign id
#    id is number which is a unique identifier for the participants
#    id is BASE_STARTER, BASE_STARTER+1 etc for participants being host for Starter
#    id is BASE_MAIN, BASE_MAIN+1  etc for participants being host for Main
#    id is BASE_DESSERT, BASE_DESSERT+1 etc for participants being host for Dessert
#    id is BASE_NIGHT, BASE_NIGHT+1 etc for participants being host for Nightfood
#    it is assigned randomly 
BASE_STARTER = 100
BASE_MAIN = 200
BASE_DESSERT = 300
BASE_NIGHT = 400
idS = []; idM = []; idD = []; idN = []
for n in range (0, oneFourth):
    idS.append(BASE_STARTER + n)
    idM.append(BASE_MAIN + n)
    idD.append(BASE_DESSERT + n)
    idN.append(BASE_NIGHT + n)
idSShuffled = list(idS)
idMShuffled = list(idM)
idDShuffled = list(idD)
idNShuffled = list(idN)
random.shuffle(idSShuffled)
random.shuffle(idMShuffled)
random.shuffle(idDShuffled)
random.shuffle(idNShuffled)
ixS = 0; ixM = 0; ixD = 0; ixN = 0
for p in participants:
    if p.isHostFor(COURSE_STARTER): p.setId(idSShuffled[ixS]); ixS += 1
    if p.isHostFor(COURSE_MAIN): p.setId(idMShuffled[ixM]); ixM += 1
    if p.isHostFor(COURSE_DESSERT): p.setId(idDShuffled[ixD]); ixD += 1
    if p.isHostFor(COURSE_NIGHT): p.setId(idNShuffled[ixN]); ixN += 1
assert ixS == oneFourth, "error when assigning idSShuffled, ixS = %s" % ixS
assert ixM == oneFourth, "error when assigning idMShuffled, ixM = %s" % ixM
assert ixD == oneFourth, "error when assigning idDShuffled, ixD = %s" % ixD
assert ixN == oneFourth, "error when assigning idNShuffled, ixN = %s" % ixN
logging.info("DONE with: Assign id")


# Assign guests for the courses

# helper function:
#     get index from id
#     p is the participants
def getIxById(p, id):
    foundIndex = -1
    for n in range(0, len(p)):
        if p[n].getId() == id:
            foundIndex = n
    return foundIndex

# helper function: rotates an array and returns a value
# args:
#     a: an array
#     steps: number of steps to rotate the items in array a to the right
#     i: index
# returns:
#     the item of a at index i after a is rotated
# note:
#     a is not affected
def getItemRotated(a, steps, i):
    assert i < len(a), "FATAL: index i is out of range"
    return a[(i - steps + len(a)) % len(a)]

# Assign guests for each participant that is host for Starter
for n in range(0, oneFourth):
    hostId = idS[n]
    ix = getIxById(participants, hostId)
    assert ix >= 0, "getIxById returned error (-1)"
    participants[ix].addGuest(idM[n])
    participants[ix].addGuest(idD[n])
    participants[ix].addGuest(idN[n])
    
# Assign guests for each participant that is host for Main
for n in range(0, oneFourth):
    hostId = getItemRotated(idM, 1, n)
    ix = getIxById(participants, hostId)
    assert ix >= 0, "getIxById returned error (-1)"
    participants[ix].addGuest(getItemRotated(idS, 0, n))
    participants[ix].addGuest(getItemRotated(idD, 2, n))
    participants[ix].addGuest(getItemRotated(idN, 3, n))

# Assign guests for each participant that is host for Dessert
for n in range(0, oneFourth):
    hostId = getItemRotated(idD, 4, n)
    ix = getIxById(participants, hostId)
    assert ix >= 0, "getIxById returned error (-1)"
    participants[ix].addGuest(getItemRotated(idS, 0, n))
    participants[ix].addGuest(getItemRotated(idM, 2, n))
    participants[ix].addGuest(getItemRotated(idN, 6, n))  

# Assign guests for each participant that is host for Nightfood
for n in range(0, oneFourth):
    hostId = getItemRotated(idN, 9, n)
    ix = getIxById(participants, hostId)
    assert ix >= 0, "getIxById returned error (-1)"
    participants[ix].addGuest(getItemRotated(idS, 0, n))
    participants[ix].addGuest(getItemRotated(idM, 3, n))
    participants[ix].addGuest(getItemRotated(idD, 6, n)) 
logging.info("DONE with: Assign guests for the courses");

    
# Verify that any participant meet any other participant at most once
# Verify that each participant meet 12 others
# Also create file who-meets-who.txt in out directory
allIds = []
allIds.extend(idS); allIds.extend(idM); allIds.extend(idD); allIds.extend(idN)
fpath = os.path.join(args.outDir, "who-meets-who.txt")
f_whoMeetsWho=open(fpath, "w") 
for id in allIds:
    logging.info("Verifying for id: %s" % id)
    meets = []
    for p in participants:
        if p.getId() == id:
            meets.extend(p.getGuests())
    for p in participants:
        if id in p.getGuests():
            meets.append(p.getId())
            otherGuests = list(p.getGuests())
            otherGuests.remove(id)
            meets.extend(otherGuests)
    f_whoMeetsWho.write("%s meets %s \r\n" % (id, sorted(meets)))
    assert len(meets) == 12, "participant with id = %s did not meet nine others, meets = %s" % (id, meets)
    assert len(set(meets)) == len(meets), "participant with id = %s: two participants meet more than once, meets = %s" % (id, meets)
f_whoMeetsWho.close()
logging.info("DONE with: Verify that any participant meet any other participant at most once")


# Generate helper file for the organizer so he/she can easily see hosts and guests for all courses
fpath = os.path.join(args.outDir, "hosts-and-guests.txt")
f = open(fpath, "w") 
for course in courses:
    f.write("=============== Värdar för %s ===============\r\n" % course)
    for p in participants:
        if p.isHostFor(course):
            f.write("\r\n(id=%s) %s %s på %s har dessa gäster:\r\n" % (p.getId(), p.getName(), p.getFamilyName(), p.getAddress()))
            for guestId in p.getGuests():
                ix = getIxById(participants, guestId)
                f.write("\t\t(id=%s) %s %s\r\n" % (participants[ix].getId(),
                                                   participants[ix].getName(),
                                                   participants[ix].getFamilyName()))        
    f.write("\r\n\r\n")
f.close()
logging.info("DONE with: Generate helper file for the organizer so he/she can easily see hosts and guests for all courses")


# Generate email1
fpath = os.path.join(args.outDir, "email1.txt")
f = open(fpath, "w")
f.write("This file is the email which will be sent to the participants.\r\n")
f.write("With this email the participant will know which course they shall be host for\r\n")
f.write("and the special food requirements for its guests.\r\n\r\n")
for p in participants:
   f.write("To: %s\r\n" % p.getEmail())
   f.write("Subject: Inbjudan till cykelfest\r\n")
   f.write("Text:\r\n")
   f.write("Du och din partner ska vara värd för %s.\r\n" % p.getCourse())
   f.write("Allergier, vegeterian eller andra krav på maten för dina gäster:\r\n")
   guestNr = 1
   for guestId in p.getGuests():
      ix = getIxById(participants, guestId)
      f.write("Gäst %s: %s\r\n" % (guestNr, participants[ix].getSpecialFoodPerson1()))
      guestNr = guestNr + 1
      f.write("Gäst %s: %s\r\n" % (guestNr, participants[ix].getSpecialFoodPerson2()))
      guestNr = guestNr + 1
   f.write("\r\n\r\n")
f.close()
logging.info("DONE with: Generate email1")


# Generate letter1
for p in participants:
   if p.isHostFor(COURSE_STARTER):
      for guestId in p.getGuests():
         ix = getIxById(participants, guestId)
         fname = "letter1_" + participants[ix].getName() + participants[ix].getFamilyName() + ".txt"
         fpath = os.path.join(args.outDir, fname)
         f = open(fpath, "w")
         f.write("Brev till: %s %s\r\n" % (participants[ix].getName(), participants[ix].getFamilyName()))
         f.write("Förrätt på: %s\r\n" % p.getAddress())
         f.write("\r\n") # Nice if you cat all such files
         f.close()
logging.info("DONE with: Generate letter1")


# Generate letter2
for p in participants:
   if p.isHostFor(COURSE_MAIN):
      for guestId in p.getGuests():
         ix = getIxById(participants, guestId)
         fname = "letter2_" + participants[ix].getName() + participants[ix].getFamilyName() + ".txt"
         fpath = os.path.join(args.outDir, fname)
         f = open(fpath, "w")
         f.write("Brev till: %s %s\r\n" % (participants[ix].getName(), participants[ix].getFamilyName()))
         f.write("Huvudrätt på: %s\r\n" % p.getAddress())
         f.write("\r\n") # Nice if you cat all such files
         f.close()
logging.info("DONE with: Generate letter2")


# Generate letter3, letter3.1, letter3.2 and letter3.3
for p in participants:
   if p.isHostFor(COURSE_MAIN):
      fname = "letter3_" + p.getName() + p.getFamilyName() + ".txt"
      fpath = os.path.join(args.outDir, fname)
      f = open(fpath, "w")
      f.write("Brev till: %s %s\r\n" % (p.getName(), p.getFamilyName()))
      f.write("Nedan finns tre brev som ska delas ut när det är dags att\r\n")
      f.write("cykla vidare till efterrätten. Klipp itu pappret\r\n")
      f.write("och dela ut till respektive mottagare\r\n")
      attendees = []
      attendees.append(p.getId())
      attendees.extend(p.getGuests())
      for a in attendees:
         ix = getIxById(participants, a)
         for p2 in participants:
            if p2.isHostFor(COURSE_DESSERT) and a in p2.getGuests():
               f.write("\r\n\r\n\r\n\r\n\r\n")
               f.write("----------------------- klipp längs med denna linjen ---------------------\r\n")
               f.write("\r\n\r\n")
               f.write("Brev till: %s %s\r\n" % (participants[ix].getName(), participants[ix].getFamilyName()))
               f.write("Efterrätt på: %s\r\n" % p2.getAddress())
      f.close()
logging.info("DONE with: Generate letter3, letter3.1, letter3.2 and letter3.3")
