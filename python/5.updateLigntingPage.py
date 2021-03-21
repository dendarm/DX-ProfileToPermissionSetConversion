from xml.etree import ElementTree as ET
import copy
import lxml.etree
import os, shutil
import sys

# Set global variables

NS = {"sf": "http://soap.sforce.com/2006/04/metadata"}
parser = lxml.etree.XMLParser(remove_blank_text=True)
appPath = "../force-app/main/default/applications/"
appSavePath = "../transform/main/default/applications/"
configPath = "../config/config.xml"

# Check  whether profiles are present in config.xml
configFile = lxml.etree.parse(configPath, parser)
configRoot = configFile.getroot()

profileList = list()

for fullProfile in configFile.xpath('//fullProfile'):
    profileList.append(fullProfile.text)

for platProfile in configFile.xpath('//platformProfile'):
    profileList.append(platProfile.text)

inputOldProfileName = configFile.xpath('//originalProfile/text()')

if len(inputOldProfileName) > 1:
    print("found more than 1 original profile, please check config/config.xml before trying again")
    quit()

#User input and filename variables

updateLightningPages = input("review Lightning App page assignments? (y/n)")

if updateLightningPages == "y"

    inputAppName = input ("Enter the apps that need to be modified: If more than one app needs to be processed, use a comma separated list (eg app1,app2): ")

    if inputOldProfileName:
        print("profiles to be converted loaded from config.xml: " +str(inputOldProfileName))
    else:
        inputOldProfileName = input ("Enter the name of the profile to be replaced: ")

    if len(profileList) > 0:
        print("profiles to be converted loaded from config.xml: " +str(profileList))
    else:
        inputNewProfileName = input ("Enter the name of the profiles to be added. If the old profile needs to be replaced by more than one profile use a comma separated list (eg profile1,profile2): ")


    #Test variables

    #inputAppName = "PTF"
    #appSaveName = "WAZA3.xml"
    #inputOldProfileName = "BC QA RUL"
    #inputNewProfileName = "Zorro2, Zorro 1"
    #appName = inputAppName + ".app-meta.xml"

    # string to list

    if len(profileList) < 0:
        profileList = inputProfileName.split(",")

    appList = inputAppName.split(",")
    numApps = len(appList)
    numProfiles = len(profileList)

    for app in appList:
        appName = app.strip()+ ".app-meta.xml"

        # Load and parser the XML   

        permTree = lxml.etree.parse(appPath + appName, parser)
        root = permTree.getroot()

        # paths and variables

        varPathRemoval = "//sf:profileActionOverrides[.//sf:profile/text() != '" + inputOldProfileName[0] + "']"
        varPathOldProfile = "//sf:profileActionOverrides[.//sf:profile/text() = '" + inputOldProfileName[0] + "']"
        varPathTransform = "//sf:profileActionOverrides/sf:profile[..//sf:profile = '" + inputOldProfileName[0] + "']"
        root = permTree.getroot()

        # Remove all profiles from the app except the one we're working with

        for removeProfile in permTree.xpath(varPathRemoval, namespaces=NS):
            removeProfile.getparent().remove(removeProfile)

        for removeActionOverride in permTree.xpath('//sf:actionOverrides', namespaces=NS):
            removeActionOverride.getparent().remove(removeActionOverride)

        # Transform XML to include new profile references

        if numProfiles == 1:

            for transformProfile in permTree.xpath(varPathTransform, namespaces=NS):
                transformProfile.text = inputNewProfileName[0]

        else:
            for profile in profileList:
                for transformProfile in permTree.xpath(varPathTransform, namespaces=NS):
                    insertPosition = permTree.find('//sf:tabs', namespaces = NS)
                    index = root.index(insertPosition)
                    copyElem = copy.deepcopy(transformProfile.getparent())

                    profileElem = lxml.etree.Element("profile")
                    profileElem.text = profile
                    transformProfile.getparent().replace(transformProfile, profileElem)
                    
                    root.insert(index, copyElem)
                    

        # Remove the references to the old profile

        for removeOldProfile in permTree.xpath(varPathOldProfile, namespaces=NS):
            removeOldProfile.getparent().remove(removeOldProfile)        
            
                
        # Save the newly created Permission Set

        permTree.write(appSavePath + appName, pretty_print=True, encoding='UTF-8', xml_declaration=True)

        print("created new file " + appName + " in location " + appSavePath)



