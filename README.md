# Third-Party Software Notice

This project includes [PDF.js](https://github.com/mozilla/pdf.js), which is licensed under the Apache License 2.0.

## PDF.js License

Copyright © 2011 Mozilla Foundation.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


> This project has used PDF.js since **[March 15, 2025]**. Original licence can be found in /static/pdfjs folder.

# How to start playing with the code
### Installation
1. Install VSCode
2. open VSCode and install these Extensions:
- SQLite Viewer
- Python
- Pylance
- Python Enviroments
- pip installer
(it is also recommended that you install python through the official website)
https://www.python.org/downloads/release/python-3112/
3. Git clone the project by clicking the green code button near the top of this page, and 'clicking the copy url to clipboard', then navigate to VSCode, select the 'Clone Git Repository', paste in the url and select a folder for the project in you file management system.
4. Open the project
5. Open the python extension tab on the left side navigation bar.
6. Move your mouse over to 'Environment Managers'
7. under the 'venv' section click to create a new environment and call it .venv
8. Hit enter until the environment starts installing.
- After your environment is added there should be an add packages to the right of its name in the 'Environment Managers'
9. Add project packages via the requirements.txt file
10. create a .env file in the main directory and add this line
- DB_NAME="Database_name.db"
- This sets the name of the database file that will be referenced throughout the project.
11. Open up a new terminal, it should have (.venv) to the left of it, and type the following commands one at a time:
- python3 start_up/02_start_database_with_vatican.py 
- python app.py # to start the flask application.
12. Open your browser and go to http://127.0.0.1:5000/login to start playing with the application.
- CTRL+C to quit/ stop the application from the terminal.