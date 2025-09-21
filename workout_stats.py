import sqlite3
from tabulate import tabulate

#Arrange and display user log data

#Display all entries in user log (with date)
#Section 1-------------------------------------------------------------------------------------------------------------------------#
def display_user_log(username):
    with sqlite3.connect("user_log.db") as connection:
        #Make rows from table so keys can be accessed
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        #Get all entries for username when a date exists (otherwise entry will be for a general exercise, not logged workout)
        cursor.execute("""
            SELECT * from user_log WHERE username = ? AND date != ""
            """, (username,))
        rows = cursor.fetchall()

        if not rows:
            print(f"There are no entries in the log for {username}")
            return

        #Only want to display data from these keys
        headers = ["id", "name", "category", "date", "duration", "distance", "weight", "reps"]
        #Turn each row into dictionary, and store as a list
        rows_as_dicts = [dict(row) for row in rows]
        #Create key/value pair for each row only containing headers desired and store new dicts in list
        new_list = [{key: row[key] for key in headers} for row in rows_as_dicts]

        print(tabulate(new_list, headers="keys", tablefmt = "grid"))
#---------------------------------------------------------------------------------------------------------------------Section 1 End#

