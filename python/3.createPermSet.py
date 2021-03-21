from xml.etree import ElementTree as ET
import lxml.etree
import os, shutil
import sys

# Set global variables

NS = {"sf": "http://soap.sforce.com/2006/04/metadata"}
parser = lxml.etree.XMLParser(remove_blank_text=True)
profilePath = "../transform/main/default/profiles/"
permSetPath = "../transform/main/default/permissionsets/"
configPath = "../config/config.xml"

# Check  whether profiles are present in config.xml

configFile = lxml.etree.parse(configPath, parser)
configRoot = configFile.getroot()

profileList = list()

for fullProfile in configFile.xpath('//fullProfile'):
    profileList.append(fullProfile.text)

for platProfile in configFile.xpath('//platformProfile'):
    profileList.append(platProfile.text)

#User input and filename variables

if len(profileList) > 0:
    print("profiles to be converted loaded from config.xml: " +str(profileList))

else:
    inputProfileName = input ("Profiles to be converted. If more than 1 needs to be created, enter them using a comma (eg. profile1, profile2): ")

inputPermSetLabel = input("Enter the label for the Permission Set to be created. If more than 1 needs to be created, enter them using a comma (eg. PermSet1, PermSet2): ")
inputPermSetName = input("Enter the API name for the Permission Set to be created. If more than 1 needs to be created, enter them using a comma (eg. APIName1, APIName2: ")
#permSetName = inputPermSetName + ".permissionset-meta.xml"
#fileName = inputProfileName + ".profile-meta.xml"

# Test variables

#inputProfileName = "Full, Platform"
#inputPermSetLabel = "Full Perm Set, Platform Perm Set"
#inputPermSetName = "FullPerm, PlatformPerm"

# strings to lists
if len(profileList) < 0:
    profileList = inputProfileName.split(",")
    
numProfiles = len(profileList)
permSetLabelList = inputPermSetLabel.split(",")
numLabels = len(permSetLabelList)
permSetAPIList = inputPermSetName.split(",")
numAPI = len(permSetAPIList)
print("profiles to be converted " +str(profileList))
print("permission set labels to be created" +str(permSetLabelList))
print("permission set API names to be created " +str(permSetAPIList))

if numProfiles != numLabels != numAPI:
    print("the number of labels entered does not match the number of API names entered. Exiting...")
    quit()
    
# Create Permission Sets
# Load and parse XML   


#permTree = lxml.etree.parse(profilePath + fileName, parser)
#root = permTree.getroot()

# insert the label into the new permission set

for profile in profileList:

    fileName = profile.strip() + ".profile-meta.xml"

    permTree = lxml.etree.parse(profilePath + fileName, parser)
    root = permTree.getroot()

    i = profileList.index(profile)

    label = lxml.etree.Element("label")
    label.text = permSetLabelList[i].strip()

    root.insert(1, label)

    # Remove unwanted sections from original profile

    for rootElem in permTree.xpath("//sf:Profile" , namespaces=NS):
        rootElem.tag = "PermissionSet"

    for cleanElements in configFile.xpath("//permissionsSetClean/name/text()"):

        print(cleanElements)

        xPath = "//sf:" +cleanElements

        print(xPath)

        for permissions in permTree.xpath(xPath, namespaces = NS):
            print(permissions)
            permissions.getparent().remove(permissions)


    # Save the newly created Permission Set

    permTree.write(permSetPath + permSetAPIList[i]+".permissionset-meta.xml", pretty_print=True, encoding='UTF-8', xml_declaration=True)
    print("created Permission Set " + permSetAPIList[i].strip() + " in location " + permSetPath +"from " +profile)

    # Add created permission set to config.xml

    permissionElement = lxml.etree.Element("permissionSet")
    permissionElement.text = permSetAPIList[i]
    configRoot.append(permissionElement)

    configFile.write(configPath, pretty_print=True, encoding='UTF-8', xml_declaration=True)

    for element in configRoot.iter():
        element.tail = None

    



