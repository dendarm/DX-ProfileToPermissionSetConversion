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
    
    for uTransferAnyCase in fxml.xpath('//sf:userPermissions[sf:name/text()="TransferAnyCase"]', namespaces=NS):
        uTransferAnyCase.getparent().remove(uTransferAnyCase)
        print("TransferAnyCase removed")
        
    for uSendSitRequest in fxml.xpath('//sf:userPermissions[sf:name/text()="SendSitRequests"]', namespaces=NS):
        uSendSitRequest.getparent().remove(uSendSitRequest)
        print("SendSitRequests removed")

    for uLightningConsole in fxml.xpath('//sf:userPermissions[sf:name/text()="LightningConsoleAllowedForUser"]', namespaces=NS):
        uLightningConsole.getparent().remove(uLightningConsole)
        print("LightningConsoleAllowedForUser removed")

    for uSubmitMacros in fxml.xpath('//sf:userPermissions[sf:name/text()="SubmitMacrosAllowed"]', namespaces=NS):
        uSubmitMacros.getparent().remove(uSubmitMacros)
        print("SubmitMacrosAllowed removed")

    for uEditCaseComments in fxml.xpath('//sf:userPermissions[sf:name/text()="EditCaseComments"]', namespaces=NS):
        uEditCaseComments.getparent().remove(uEditCaseComments)
        print("EditCaseComments removed")


    platProfile = ET.Element("platformProfile")
    platProfile.text = inputFileNamePlatformProfile.strip()
    configRoot.append(platProfile)

# Write back to the XML file
fxml.write(savePath + fileNamePlatformProfile, pretty_print=True, encoding='UTF-8', xml_declaration=True)

# Add elements to config XML

for element in configRoot.iter():
    element.tail = None

config.write("../config/config.xml", pretty_print=True, encoding='UTF-8', xml_declaration=True)









