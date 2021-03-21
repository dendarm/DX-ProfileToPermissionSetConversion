# DX-ProfileToPermissionSetConversion

This project started with a requirement to convert existing Salesforce License Profiles to Platform Licenses, while at the same time migrating the bulk of the associated permissions to Permission Sets. This meant a lot of manual work and the overall process was time consuming. I mostly wrote these scripts because I'm lazy, and now the process (excluding the retrieve and deploy of the metadata) takes less than a minute.
This code is just a first working version, and I'm sure it can be improved in many ways. 

### I am by no means a qualified developer, so use this at your own risk. Any suggestions are more than welcome.


## What this does

1.	Creates the folder tree needed to work in
2.	Asks whether a metadata retrieve is needed, skip this if you already have retrieved the metadata separately (stored under force-app)
3.	Prompts the user for which profile should be converted
4.	Prompts the user for the names of the new profiles to be created
5.	Creates permission sets based on the newly created profiles and asks for the Label and API name of the PSs to be created (the order in which you enter data is important)
6.	Removes the unwanted permissions from the newly created PSs (layoutAssignments, recordTypeVisibilities, tabVisibilities, userPermissions)
7.	Copies fieldPermissions, objectPermissions, classAccess, pageAccess, customMetadataTypeAccesses, customSettingAccesses to the new PSs
8.	Disables fieldPermissions, objectPermissions, classAccess, pageAccess, customMetadataTypeAccesses, customSettingAccesses on the new Profiles
9.	Prompts the user which lightning page assignments need to be reviewed
10.	Scans the selected applications for references to the original profile to be converted and updates it with the newly created profiles
11.	Creates a XML package based on the transformed metadata and saves it as /manifest/packageTransformed.xml


## Usage

This should be run from a DX project! [How to create a DX project](https://trailhead.salesforce.com/en/content/learn/projects/develop-app-with-salesforce-cli-and-source-control/create-salesforce-dx-project)

Clone the project or download the .zip [link](https://github.com/dendarm/DX-ProfileToPermissionSetConversion/archive/refs/heads/main.zip).

If you downloaded the zip, unzip it in an note down where you stored it.

Open Command Prompt on windows and enter:

 ```bash
cd "pathToUnzippedFolder"
```

where pathToUnzipped folder is the location to which you unzipped the contents.

Eg.

 ```bash
cd "C:\Users\JohnDoe\Downloads\DX-ProfileToPermissionSetConversion"
```

Open a command line from the folder to which you download this project and run:

```bash
../python.runAll.bat
```

or navigate to the python subfolder and double click on runAll.bat

The runAll.bat file in /python executes the individual python scripts in sequence. Each script can be launched individually, but if you mess with the order in which they need to be run, things will break.

## Dependencies and required tools

1. Salesforce DX [Download](https://developer.salesforce.com/tools/sfdxcli)
2. Python [Download](https://www.python.org/downloads/)
3. LXML library [Reference](https://pypi.org/project/lxml)

## Additional references

[Installing Python Packages](https://packaging.python.org/tutorials/installing-packages/#ensure-you-can-run-python-from-the-command-line)

[Set up Salesforce DX Trailhead](https://trailhead.salesforce.com/content/learn/modules/sfdx_app_dev/sfdx_app_dev_setup_dx)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

