#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
import os
import re
import sys
from random import randint

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
    "vegetarian",
    "allergisk mot laktos",
    "allergisk mot gluten",
    "vegetarian",
    "allergisk mot stenfrukter",
    "allergisk mot äpplen",
    "allergisk mot banan",
    "vegetarian",
    "allergisk mot kiwi",
    "allergisk mot mandel",
    "allergisk mot nötter",
    "vegetarian",
    "allergisk mot räkor",
    "allergisk mot torsk",
    "vegetarian",
    "vegetarian (äter fisk och skaldjur)",
    "allergisk mot gluten"]

desiredMeals = ["Måste ha nattamat (bor utanför Harlösa)",
    "Vill ha förrätt",
    "Vill inte ha förrätt",
    "Vill ha huvudrätt",
    "Vill inte ha huvudrätt",
    "Vill ha efterrätt",
    "Vill inte ha efterrätt",
    "Vill ha nattamat",
    "Vill inte ha nattamat"]
    
assert len(familyNames) == 40, "nbr of familyNames not equal to 40, is equal to %s" % len(familyNames)
assert len(names) == 40, "nbr of names not equal to 40, is equal to %s" % len(names)
assert len(adresses) == 40, "nbr of adresses not equal to 40, is equal to %s" % len(adresses)
assert len(emails) == 40, "nbr of emails not equal to 40, is equal to %s" % len(emails)
assert len(phoneNbrs) == 40, "nbr of phoneNbrs not equal to 40, is equal to %s" % len(phoneNbrs)

# Parse command line arguments
argparser = argparse.ArgumentParser(description="Generates test data (csv file) which can be used as input for combine-safar-dinner.py")
argparser.add_argument("-o", "--out",
                        required = True,
                        dest = "outFileName",
                        help = "File that will be created.")
args = argparser.parse_args()

def getPreferredMeal():
    if randint(0, 1) == 1:
        return ("Inget önskemål")
    else:
        return desiredMeals[randint(0, len(desiredMeals) - 1)]

def getSpecialFood():
    if randint(0, 1) == 1:
        return ("")
    else:
        return specialFood[randint(0, len(specialFood) - 1)]

# generate one .csv file with all participant, in the same format as
# a Responses -> Download .csv file from Google forms (https://docs.google.com/forms)
f=open(args.outFileName, "w")

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
f.write(header)

# Print data in the csv file
TIMESTAMP = "2017/09/07 10:03:37 pm EET" # dummy timestamp
for i in range (0, len(familyNames)):
    f.write("\r\n")

    f.write("\"")
    f.write(TIMESTAMP)
    f.write("\",")

    f.write("\"")
    f.write(familyNames[i])
    f.write("\",")

    f.write("\"")
    f.write(names[i])
    f.write("\",")

    f.write("\"")
    f.write(adresses[i])
    f.write("\",")

    f.write("\"")
    f.write(emails[i])
    f.write("\",")

    f.write("\"")
    f.write(phoneNbrs[i])
    f.write("\",")

    f.write("\"")
    f.write(getPreferredMeal())
    f.write("\",")

    f.write("\"")
    f.write(getSpecialFood())
    f.write("\",")

    f.write("\"")
    f.write(getSpecialFood())
    f.write("\"")

f.close()
