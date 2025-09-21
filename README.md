# Simple Workout Tracker

## Author: Sapna Mehta-Gertz

### Description
This simple workout tracker is a project I built for the CS50 python course and am continuing to improve. I chose to make this project because I recently started exercising with weights in a gym and wanted a simple way to track my consistency and progress to stay motivated!

The program is a command-line application that currently has the following functionality:
    1. Create, store, and retrieve user profiles
    2. Add a workout to your own log from an existing database (see below for data source credit), from your own existing log, or create a new exercise
    3. Edit or delete entries from your log
    4. View your complete log

### How To Use

Once installed, open the command terminal and navigate to the unzipped folder path.

Run the program with: `python project.py`

The program will then give you prompts and instructions to interact with it via the commmand line.


### Installation and requirements
Requirements:
    - Python 3.13 (https://www.python.org/downloads/). Make sure that 'python' and 'pip' commands work from your terminal (you may need to add python to your system PATH)

Install Workout Tracker project:
- Download zip file from github; unzip file
- Install tabulate library:
    + install from requirements.txt
        ```
        pip install -r requirements.txt
        ```
    + or install from tabulate
        ```
        pip install tabulate
        ```
The program should now be ready to run from the command line


### Data Source
The exercise data users have the ability to filter/search and add to their own log was obtained from the Free Exercise DB (https://github.com/yuhonas/free-exercise-db) by Clint Plummer, which is released under The Unlicense (https://unlicense.org/). The original dataset comes from exercises.json by Ollie Jennings (https://github.com/wrkout/exercises.json) as credited in the Free Exercise DB repository.


### Future improvements

1. Expanded usability and customizability of user log
   a. Filtering user's own log for display (e.g., searching for all 'squats' entried in your log to track progress on that particular exercise, or searching all exercises logged in particular time period)
   b. Display summary information from user log (e.g., sum of exercises logged - total and conditional on criteria)
   c. Include additional keys in user log that can be used for display and filtering (e.g., primary muscle groups used for exercises)
2. Allow user to select multiple values for each filter category
3. Random exercise recommendation based on user criteria
4. Test files
