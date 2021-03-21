from xml.etree import ElementTree as ET
import lxml.etree
import os, shutil
import sys

# Set global variables

NS = {"sf": "http://soap.sforce.com/2006/04/metadata"}
parser = lxml.etree.XMLParser(remove_blank_text=True)
profilePath = "../transform/main/default/profiles/"
configPath = "../config/config.xml"

# Check  whether profiles are present in config.xml

configFile = lxml.etree.parse(configPath, parser)
configRoot = configFile.getroot()

profileList = list()

for fullProfile in configFile.xpath('//fullProfile'):
    profileList.append(fullProfile.text)

for platProfile in configFile.xpath('//platformProfile'):
    profileList.append(platProfile.text)
    print(len(profileList))

#User input and filename variables

if len(profileList) > 0:
    print("profiles to be cleaned loaded from config.xml: " +str(profileList))
else:
    inputProfileName = input ("Profiles to be cleaned. If more than 1 needs to be created, enter them using a comma (eg. profile1, profile2):  ")

# string to list
if len(profileList) < 0:
    profileList = inputProfileName.split(",")

numProfiles = len(profileList)


# Clean profiles and remove unwanted metadata

# Parse XML file

for profile in profileList:

    fileName = profile.strip() + ".profile-meta.xml"
    i = profileList.index(profile)

    tree = lxml.etree.parse(profilePath + fileName, parser)
    root = tree.getroot()

    for profileClean in configFile.xpath('//profileClean/name/text()'):

        for cleanElement in tree.xpath(profileClean, namespaces=NS):
            print(cleanElement)
            cleanElement.text = "false"

    # Write back to the XML file
    tree.write(profilePath + fileName, pretty_print=True, encoding='UTF-8', xml_declaration=True)


