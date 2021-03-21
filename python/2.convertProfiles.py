from lxml import etree as ET
import os, shutil
import sys

# Global variables

NS = {"sf": "http://soap.sforce.com/2006/04/metadata"}
parser = ET.XMLParser(remove_blank_text=True)

# user input variables
inputFileName = input("Enter the name of the profile to be converted: ")
inputFileNameFullProfile = input("Enter new name for Salesforce Profile. Leave blank if none: ")
inputFileNamePlatformProfile = input("Enter new name for Salesforce Platform Profile. Leave blank if none: ")

# file and path variables
savePath = "../transform/main/default/profiles/"
fileName = inputFileName + ".profile-meta.xml"
fileNameFullProfile = inputFileNameFullProfile + ".profile-meta.xml"
fileNamePlatformProfile = inputFileNamePlatformProfile + ".profile-meta.xml"
configPath = "../config/config.xml"

# Parse XML files
fxml = ET.parse("../force-app/main/default/profiles/" + fileName, parser)
config = ET.parse("../config/config.xml", parser)
configRoot = config.getroot()
originalProfile = ET.Element("originalProfile")
originalProfile.text = inputFileName

# Save original profile name to config.xml
configRoot.append(originalProfile)

# Write back to the XML files
fxml.write(savePath + fileNameFullProfile, pretty_print=True, encoding='UTF-8', xml_declaration=True)
fullProfile = ET.Element("fullProfile")
fullProfile.text = inputFileNameFullProfile
configRoot.append(fullProfile)

# Look for userLicense type Salesforce and replace with Salesforce Platform

if inputFileNamePlatformProfile: 

# Set user license to Salesforce Platform    
    for elem in fxml.xpath('//sf:userLicense[text()="Salesforce"]' , namespaces=NS):

        userLicense = ET.Element("userLicense")
        userLicense.text = "Salesforce Platform"
        
        elem.getparent().replace(elem, userLicense)

# Remove user permission that are not compatible with Platform licences
    
    for cleanUserPermissions in config.xpath("//userPermissionClean/name/text()"):

        xPath = '//sf:userPermissions[sf:name/text()= "' +cleanUserPermissions + '"]'

        for userPermission in fxml.xpath(xPath, namespaces = NS):
            print(cleanUserPermissions + " removed")
            userPermission.getparent().remove(userPermission)


    platProfile = ET.Element("platformProfile")
    platProfile.text = inputFileNamePlatformProfile.strip()
    configRoot.append(platProfile)

# Write back to the XML file
fxml.write(savePath + fileNamePlatformProfile, pretty_print=True, encoding='UTF-8', xml_declaration=True)

# Add elements to config XML

for element in configRoot.iter():
    element.tail = None

config.write("../config/config.xml", pretty_print=True, encoding='UTF-8', xml_declaration=True)









