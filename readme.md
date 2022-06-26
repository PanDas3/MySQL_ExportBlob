# Project Name
* MySQLExportBlob - version 1.2.71

Project Date: June 2021

My first bigger project


## Additional infromation

- Icon from: https://icon-icons.com/icon/business-application-download-download-database-the-database/1817

- The project consisted in exporting files from the database for its liquidation and it's services (technological debt). An external company priced such a program at 24 MD, I did it maybe crookedly, but in 11MD with tests and for free :)
- I wrote this program after my job, because it is an element of my self-development.


## Table of Contents
* [General Info](#general-information)
* [Additional infromation](#additional-infromation)
* [General Information](#general-information)
* [Technologies Used](#technologies-used)
* [Usage](#usage)
* [Project Status](#project-status)
* [Contact](#contact)
<!-- * [License](#license) -->


## General Information
The program has:
- Getting params from configuration file
- Connecting to MySQL
- Save blob column to file
- Change xml (blob file)
- Building HTML from xml and xslt
- Logged status
- Validation for this same filename in database
- Second verification of the correctness of the export (test_finish.py)


## Technologies Used
- Python - version 3.9.4
- PyMySQL - version 0.10.1 (required for my assignment, not higher)
- LXML - version 4.6.3
- ConfigParser - version 5.0.2
- Logger - version 2.3.0
- PyInstaller - version 4.2

<!--
## Features
None


## Screenshots
![Example screenshot](./img/screenshot.png)


## Setup
What are the project requirements/dependencies? Where are they listed? A requirements.txt or a Pipfile.lock file perhaps? Where is it located?

Proceed to describe how to install / setup one's local environment / get started with the project.
-->

## Usage
If you would like to run from script:
1. Run main.py
2. Complete config.ini
3. Run main.py
4. Look at the log file
5. After finish all exports edit test_finish.py 
`sql_count_query = "SELECT count(id) FROM base.table where id = "`
6. Run test_finish.py

If u would like to run EXE:

Generate EXE file - CMD ->
```batch
pip install pyinstaller --proxy http://user:pass@proxy.pl:3128
cd Building
pyinstaller MySQL_ExportBlob.spec
```

1. Run MySQL_Export.exe
2. Complete config.ini
3. Run again MySQL_Export.exe
4. Look at the log file
5. After finish all exports edit test_finish.py 
`sql_count_query = "SELECT count(id) FROM base.table where id = "`
6. Run test_finish.py

## Project Status
Project is: _completed and discontinue_

<!-- _complete_ / _no longer being worked on_ (and why) -->

<!-- 
## Room for Improvement
No plans
-->

## Contact
Created by [@Majster](mailto:rachuna.mikolaj@gmail.com)