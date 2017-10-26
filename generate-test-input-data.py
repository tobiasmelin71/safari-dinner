#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# status (TODO/DONE): DONE

import argparse
import logging
import os
import re
import sys

# Configuration
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

familyNames = ["Andersson",
    "Johansson",
    "Karlsson",
    "Nilsson",
    "Eriksson",
    "Larsson",
    "Olsson",
    "Persson",
    "Svensson",
    "Gustafsson",
    "Pettersson",
    "Jonsson",
    "Jansson",
    "Hansson",
    "Bengtsson",
    "Jönsson",
    "Jakobsson",
    "Magnusson",
    "Olofsson",
    "Axelsson",
    "Mattsson",
    "Fredriksson",
    "Henriksson",
    "Danielsson",
    "Håkansson",
    "Gunnarsson",
    "Samuelsson",
    "Fransson",
    "Isaksson",
    "Arvidsson",
    "Claesson",
    "Mårtensson",
    "Eliasson",
    "Pålsson",
    "Hermansson",
    "Abrahamsson",
    "Martinsson",
    "Andreasson",
    "Månsson",
    "Kjällsson"]

names = ["Molly",
    "Alva",
    "Ellen",
    "Stella",
    "Clara",
    "Linnea",
    "Emma",
    "Signe",
    "Isabelle",
    "Vera",
    "Leah",
    "Emilia",
    "Ester",
    "Sara",
    "Nova",
    "Ines",
    "Nellie",
    "Selma",
    "Elise",
    "Sofia",
    "Frans",
    "Jonathan",
    "Aron",
    "Kian",
    "Nicolas",
    "Julian",
    "Simon",
    "Vilgot",
    "David",
    "Elis",
    "Ivar",
    "Elvin",
    "Joel",
    "John",
    "Acke",
    "Samuel",
    "Daniel",
    "Åke",
    "Ärling",
    "Örjan"]

adresses = ["Blockmakargatan 1",
    "Borstbindargatan 2",
    "Brandvaktgatan 3",
    "Brevmålargatan 4 a",
    "Byvaktargatan 5",
    "Docentgatan 6",
    "Dragaregatan 7",
    "Drottninggatan 8",
    "Gelbgjutargatan 9",
    "Generalsgatan 10",
    "Glasförargatan 11",
    "Gulddragargatan 5B",
    "Häradsmålargatan 24",
    "Kaptensgatan 34",
    "Kungsgatan 61",
    "Lumpsamlargatan 25",
    "Luntmakargatan 73",
    "Lykttändargatan 12",
    "Lådmakargatan 35",
    "Majorgatan 24",
    "Nålmakargatan 23",
    "Paradisgatan 14",
    "Perukmakargatan 98",
    "Profossgatan 12",
    "Provinsialläkargatan 3",
    "Rackargatan 23",
    "Räksmörgåsgatan 12",
    "Salpetersjudargatan 54",
    "Saltmätargatan 8",
    "Saturnusgatan 3",
    "Saxofongatan 6",
    "Snörmakargatan 4",
    "Sockerbagargatan 1",
    "Telegrafistgatan 43",
    "Tolagsskrivargatan 103",
    "Trubadurgatan 32",
    "Tunnbindargatan 75",
    "Valackargatan 32",
    "van Dries gata 1",
    "Vågmästargatan 3"]

emails = ["molly@hotmail.com",
    "alva@hotmail.com",
    "ellen@hotmail.com",
    "stella@hotmail.com",
    "clara@hotmail.com",
    "linnea@hotmail.com",
    "emma@hotmail.com",
    "signe@hotmail.com",
    "isabelle@hotmail.com",
    "vera@hotmail.com",
    "leah@hotmail.com",
    "emilia@hotmail.com",
    "ester@hotmail.com",
    "sara@hotmail.com",
    "nova@hotmail.com",
    "ines@hotmail.com",
    "nellie@hotmail.com",
    "selma@hotmail.com",
    "elise@hotmail.com",
    "sofia@hotmail.com",
    "frans@hotmail.com",
    "jonathan@hotmail.com",
    "aron@hotmail.com",
    "kian@hotmail.com",
    "nicolas@hotmail.com",
    "julian@hotmail.com",
    "simon@hotmail.com",
    "vilgot@hotmail.com",
    "david@hotmail.com",
    "elis@hotmail.com",
    "ivar@hotmail.com",
    "elvin@hotmail.com",
    "joel@hotmail.com",
    "john@hotmail.com",
    "acke@hotmail.com",
    "samuel@hotmail.com",
    "daniel@hotmail.com",
    "thor@hotmail.com",
    "maximilian@hotmail.com",
    "rasmus@hotmail.com"]

phoneNbrs = ["0703135275",
    "0703451271",
    "0703730938",
    "0703213765",
    "0703264784",
    "0703319876",
    "0703277333",
    "0703132681",
    "0703590407",
    "0703322397",
    "0703566095",
    "0703636958",
    "0703321156",
    "0703508777",
    "0703328741",
    "0703758999",
    "0703094296",
    "0703012440",
    "0703347199",
    "0703421618",
    "0703830525",
    "0703015620",
    "0703856688",
    "0703235939",
    "0703632704",
    "0703012144",
    "0703894448",
    "0703370617",
    "0703167452",
    "0703510644",
    "0703585963",
    "0703247863",
    "0703771183",
    "0703572341",
    "0703648613",
    "0703340223",
    "0703140115",
    "0703795943",
    "0703437045",
    "0703072199"]

specialFood = ["vegetarian",
    "allergisk mot nötter och mandel",
    "allergisk mot laktos",
    "allergisk mot gluten",
    "allergisk mot stenfrukter"]

meals = ["förrätt",
    "huvudrätt",
    "efterrätt",
    "nattamat"]

mustHaveText = "Måste ha nattamat (bor utanför Harlösa)"
dontCareText = "Inget önskemål" 
wantTextIngress = "Vill ha "
notWantTextIngress = "Vill inte ha "

# Pre-generated random values from 0 to 29
MAX_RAND = 29
MIN_RAND = 0
RAND_SPAN = MAX_RAND - MIN_RAND
randomPreGenerated = [" 14 ",
    " 20 ",
    " 3 ",
    " 28 ",
    " 27 ",
    " 3 ",
    " 12 ",
    " 15 ",
    " 7 ",
    " 0 ",
    " 2 ",
    " 1 ",
    " 4 ",
    " 3 ",
    " 0 ",
    " 12 ",
    " 29 ",
    " 19 ",
    " 7 ",
    " 14 ",
    " 23 ",
    " 9 ",
    " 29 ",
    " 0 ",
    " 20 ",
    " 7 ",
    " 12 ",
    " 0 ",
    " 10 ",
    " 6 ",
    " 17 ",
    " 8 ",
    " 6 ",
    " 20 ",
    " 22 ",
    " 6 ",
    " 1 ",
    " 0 ",
    " 8 ",
    " 20 "]

def getMyRandom(i, seed):
    return int(randomPreGenerated[(i + seed) % len(randomPreGenerated)])
    

assert len(familyNames) == 40, "nbr of familyNames not equal to 40, is equal to %s" % len(familyNames)
assert len(names) == 40, "nbr of names not equal to 40, is equal to %s" % len(names)
assert len(adresses) == 40, "nbr of adresses not equal to 40, is equal to %s" % len(adresses)
assert len(emails) == 40, "nbr of emails not equal to 40, is equal to %s" % len(emails)
assert len(phoneNbrs) == 40, "nbr of phoneNbrs not equal to 40, is equal to %s" % len(phoneNbrs)
assert len(randomPreGenerated) == 40, "nbr of randomPreGenerated not equal to 40, is equal to %s" % len(randomPreGenerated)


# Parse command line arguments
argparser = argparse.ArgumentParser(description="Generates test data which can be used as input for combine-safar-dinner.py")
argparser.add_argument("-o", "--out-dir",
                        required = True,
                        dest = "outdir",
                        help = "Directory that will be created. It will contain all generated files.")
args = argparser.parse_args()
try:
    os.mkdir(args.outdir)
    logging.info("Directory %s was created." % args.outdir)
except OSError as e:
    logging.error("Failed to create directory %s. Error = %s." % (args.outdir, e.strerror))
    sys.exit(-1)


# generate text files (one per participant)
for i in range (0, len(familyNames)):
    fname = str(i).zfill(2) + ".txt"
    fpath = os.path.join(args.outdir, fname)
    f=open(fpath, "w")
    f.write("Efternamn: %s\r\n" % familyNames[i])
    f.write("Namn: %s\r\n" % names[i])
    f.write("Adress: %s\r\n" % adresses[i])
    f.write("Email: %s\r\n" % emails[i])
    f.write("Telefonnummer: %s\r\n" % phoneNbrs[i])
    f.write("Önskemål om måltid: ")

    # Simulate different "what meal they want"
    randomValue = getMyRandom(i, 31)  
    if (randomValue <= RAND_SPAN/6): 
        f.write("%s\r\n" % mustHaveText) 
    elif (randomValue <= RAND_SPAN/2):
        f.write("%s\r\n" % dontCareText)   
    else:
        randomValue = getMyRandom(i, 14)
        if (randomValue < RAND_SPAN/2):
            f.write("%s" % wantTextIngress)
        else:
            f.write("%s" % notWantTextIngress)
        randomValue = getMyRandom(i, 7)
        if (randomValue < RAND_SPAN/4):
            f.write("%s\r\n" % meals[0])
        elif (randomValue < RAND_SPAN/2):
            f.write("%s\r\n" % meals[1])
        elif (randomValue < 3*RAND_SPAN/4):
            f.write("%s\r\n" % meals[2])
        else:
            f.write("%s\r\n" % meals[3])

    # Simulate different food requirements
    randomValue = getMyRandom(i, 0)
    if (randomValue < 5):
        f.write("Vegetarian, allergier eller liknande (jag): %s\r\n" % specialFood[randomValue])
    else:
        f.write("Vegetarian, allergier eller liknande (jag): \r\n")
    randomValue = getMyRandom(i, 17)
    if (randomValue < 5):
        f.write("Vegetarian, allergier eller liknande (make/maka/sambo/...): %s\r\n" % specialFood[randomValue])
    else:
        f.write("Vegetarian, allergier eller liknande (make/maka/sambo/...): \r\n")

    f.write("\r\n") # comes handy if we run cat * in the out directory
    f.close()


# generate one .csv file with all participant, in the same format as
# a Responses -> Download .csv file from Google forms (https://docs.google.com/forms)
csvFilePath = os.path.join(args.outdir, "all.csv")
csvFile=open(csvFilePath, "w")

# Print header in the csv file
header = "\"Timestamp\","
header += "\"Efternamn\","
header += "\"Namn\","
header += "\"Adress\","
header += "\"Email\","
header += "\"Telefonnummer\","
header += "\"Önskemål om måltid\","
header += "\"Vegetarian, allergier eller liknande (jag)\","
header += "\"Vegetarian, allergier eller liknande (make/maka/sambo/...)\""
csvFile.write(header)

# Print data in the csv file
for i in range (0, len(familyNames)):
    txtFileName = str(i).zfill(2) + ".txt"
    txtFilePath = os.path.join(args.outdir, txtFileName)
    txtFile=open(txtFilePath, "r")
    txtToWrite = "\r\n"
    txtToWrite = txtToWrite + "\"2017/09/07 10:03:37 pm EET\"," # dummy timestamp
    for line in txtFile:
        if len(line.rstrip('\n\r')) == 0:
            continue # skip empty lines
        txtToWrite = txtToWrite + "\""
        # Removes everything before ": " and removes line feed and carriage return   
        txtToWrite = txtToWrite + (line.split(': ', 1)[-1]).rstrip('\n\r') 
        txtToWrite = txtToWrite + "\","
    txtToWrite = txtToWrite[:-1] # remove last character (an unwanted comma)
    csvFile.write(txtToWrite)
    txtFile.close()
csvFile.close()
