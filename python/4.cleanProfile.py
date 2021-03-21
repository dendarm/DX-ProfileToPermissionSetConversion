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

    for fieldRead in tree.xpath('//sf:fieldPermissions/sf:readable[../sf:readable/text()="true"]', namespaces=NS):
        fieldRead.text = "false"

    for fieldEdit in tree.xpath('//sf:fieldPermissions/sf:editable[../sf:editable/text()="true"]', namespaces=NS):
        fieldEdit.text = "false"

    for objCreate in tree.xpath('//sf:objectPermissions/sf:allowCreate[../sf:allowCreate/text()="true"]', namespaces=NS):
        objCreate.text = "false"
        print("object create permissions set to false")

    for objDelete in tree.xpath('//sf:objectPermissions/sf:allowDelete[../sf:allowDelete/text()="true"]', namespaces=NS):
        objDelete.text = "false"
        print("object delete permissions set to false")

    for objEdit in tree.xpath('//sf:objectPermissions/sf:allowEdit[../sf:allowEdit/text()="true"]', namespaces=NS):
        objEdit.text = "false"
        print("object edit permissions set to false")

    for objRead in tree.xpath('//sf:objectPermissions/sf:allowRead[../sf:allowRead/text()="true"]', namespaces=NS):
        objRead.text = "false"
        print("object read permissions set to false")

    for objModAll in tree.xpath('//sf:objectPermissions/sf:modifyAllRecords[../sf:modifyAllRecords/text()="true"]', namespaces=NS):
        objModAll.text = "false"
        print("object modify all permissions set to false")

    for objViewAll in tree.xpath('//sf:objectPermissions/sf:viewAllRecords[../sf:viewAllRecords/text()="true"]', namespaces=NS):
        objViewAll.text = "false"
        print("object view all permissions set to false")

    for classAccess in tree.xpath('//sf:classAccesses/sf:enabled[../sf:enabled/text()="true"]', namespaces=NS):
        classAccess.text = "false"
        print("class access permissions set to false")

    for pageAccess in tree.xpath('//sf:pageAccesses/sf:enabled[../sf:enabled/text()="true"]', namespaces=NS):
        pageAccess.text = "false"
        print("VF page permissions set to false")

    for metadataAccess in tree.xpath('//sf:customMetadataTypeAccesses/sf:enabled[../sf:enabled/text()="true"]', namespaces=NS):
        metadataAccess = "false"
        print("Custom Metadata access set to false")

    for customSettingAccess in tree.xpath('//sf:customSettingAccesses/sf:enabled[../sf:enabled/text()="true"]', namespaces=NS):
        customSettingAccess = "false"
        print("Custom Settings access set to false")

# Write back to the XML file
tree.write(profilePath + fileName, pretty_print=True, encoding='UTF-8', xml_declaration=True)


