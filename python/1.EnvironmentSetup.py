import os
import shutil
import json
from lxml import etree as ET


#Make folder structure needed for project

# variables

rootDir = "../transform"
configPath = "../config/config.xml"
tempDir = "../temp"
jsonPath = "../sfdx-project.json"

parser = ET.XMLParser(remove_blank_text=True)

main = "/main"
default = "/default"
applications = "/applications"
profiles = "/profiles"
permissionsets = "/permissionsets"

# Clean up existing data in folders so nothing breaks

createFolders = input("Clean folder structure? Only select y if you want to remove leftover data from previous conversion.(y/n): ")

if createFolders == "y": 
    shutil.rmtree(rootDir)
    shutil.rmtree(tempDir)
    os.mkdir(rootDir)
    os.mkdir(rootDir + main)
    os.mkdir(rootDir + main + default)
    os.mkdir(rootDir + main + default + applications)
    os.mkdir(rootDir + main + default + profiles)
    os.mkdir(rootDir + main + default + permissionsets)
    os.mkdir(tempDir)

elif createFolders == "n":
    print("skipping folder creation")

print("cleaning config.xml...")

configFile = ET.parse(configPath, parser)

for cleanConfig in configFile.xpath('//config/originalProfile'):
    cleanConfig.getparent().remove(cleanConfig)

for cleanConfig in configFile.xpath('//config/fullProfile'):
    cleanConfig.getparent().remove(cleanConfig)

for cleanConfig in configFile.xpath('//config/platformProfile'):
    cleanConfig.getparent().remove(cleanConfig)

for cleanConfig in configFile.xpath('//config/permissionSet'):
    cleanConfig.getparent().remove(cleanConfig)

configFile.write("../config/config.xml", pretty_print=True, encoding='UTF-8', xml_declaration=True)

# retrieve metadata from source org

retrieveSource = input("retrieve metadata from org? WARNING: this might take some time depending on the org size. (y/n): ")

if retrieveSource == "y":

    sourceOrg = input("DX alias of the org to pull from: ")
    dxCommand = "sfdx force:source:retrieve -x manifest/package.xml -u " +sourceOrg

    project = {"packageDirectories":[
    {"path": "force-app",
    "default": True
    }],
    "namespace": "",
    "sfdcLoginUrl": "https://login.salesforce.com",
    "sourceApiVersion": "51.0"
    }

    with open(jsonPath, 'w') as jsonFile:
        json.dump(project, jsonFile)

    os.chdir("..")

    dxRetrieve = os.system(dxCommand)

elif retrieveSource == "n":
    print("skipping metadata retrieve")



