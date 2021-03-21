import json
import os
from shutil import copyfile

# variable definition
fileName = "../sfdx-project.json"
outPath = "./temp/package.xml"
savePath = "./manifest/packageTransformed.xml"

project = {"packageDirectories":[
{"path": "transform",
"default": True
}],
"namespace": "",
"sfdcLoginUrl": "https://login.salesforce.com",
"sourceApiVersion": "51.0"
}

with open(fileName, 'w') as jsonFile:
    json.dump(project, jsonFile)

os.chdir("..")

buildPackage = os.system('sfdx force:source:convert -r transform  -d temp')
copyfile(outPath, savePath)
