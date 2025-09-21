import sqlite3
import requests

#Fetching workout data, creating workout database, and filtering

#Workout database fetching and creation
#Section 1------------------------------------------------------------------------------------------------------------------------------#
def fetch_workout_database():
    #Make 3 attempts to fetch data, otherwise stop
    for attempt in range(3):
        try:
            #Fetch JSON from yuhonas open source exercises database on github
            request = requests.get("https://raw.githubusercontent.com/yuhonas/free-exercise-db/refs/heads/main/dist/exercises.json")
            #Check for any error in server or connection; this will raise a custom error if status code warrants it
            request.raise_for_status()
            #Store list of dictionaries
            exercise_database = request.json()
            break
        #Exceptions raised from requests (will loop through request 3 times max)
        except requests.exceptions.HTTPError as e:
            print(f"Server returned HTTP Error: {e}")
        except requests.exceptions.ConnectionError as e:
            print(f"Could not connect to the server: {e}")
    else:
        print("After 3 attempts, cannot fetch database")

    #Connect to SQLite and create database if not already existing
    with sqlite3.connect("workout_selection.db") as connection:
        cursor = connection.cursor()
        #Create table of workouts from database; create id for each entry that autoincrements
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workout_selection (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       name TEXT,
                       force TEXT,
                       level TEXT,
                       mechanic TEXT,
                       equipment TEXT,
                       primary_muscles TEXT,
                       secondary_muscles TEXT,
                       instructions TEXT,
                       category TEXT,
                       images TEXT)
        """)
        connection.commit()

        #Add each entry from fetched JSON to database
        for exercise in exercise_database:
            #Use .get to assign values, since less likely to get error for empty fields
            #Use INSERT OR IGNORE to make sure duplicate entries aren't created in case database is recreated
            cursor.execute("""
            INSERT OR IGNORE INTO workout_selection (
                            name, force, level, mechanic, equipment, primary_muscles,
                            secondary_muscles, instructions, category, images)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            #the below tuple will be inserted into respective columns (where ? is currently placeholder)
                            (
                                exercise.get("name"),
                                exercise.get("force"),
                                exercise.get("level"),
                                exercise.get("mechanic"),
                                exercise.get("equipment"),
                                #for below fields, .get will return lists, so join to create string (or if empty, join empty list)
                                ",".join(exercise.get("primaryMuscles", [])),
                                ",".join(exercise.get("secondaryMuscles", [])),
                                ",".join(exercise.get("instructions", [])),
                                exercise.get("category"),
                                ",".join(exercise.get("images", []))
                            ))
#--------------------------------------------------------------------------------------------------------------------------Section 1 End#




#Select from larger or user workout database. Functions return workout ID.
#Section 2------------------------------------------------------------------------------------------------------------------------------#

#______________________________________________Select workout from large database_______________________________________________#
def select_workout():
    while True:
        try:
            answer = input("Do you want to select an exercise from a large workout database? Y/N (If you want to quit workout selection, type the word 'quit' for any entry) ").lower()
            if answer in ["y", "yes"]:
                user_filter = filter_workout_db()

                #Query database based on filters user selects above
                base_query = "SELECT id, name, category, level, equipment, primary_muscles FROM workout_selection"
                conditions, parameters = filter_for_query(user_filter)
                if conditions:
                    #Iif there are any filters selected, the base query will be updated with all items in conditions list (joined by AND)
                    query = base_query + " WHERE " + " AND ".join(conditions)
                else:
                    answer = input("Without any filters, there are over 800 entries. Do you want to go back and use filtering? Y/N? ").strip().lower()
                    if answer not in ["y", "yes", "quit"]:
                        query = base_query
                    else:
                        #Offer filter selection again if user types y/yes/quit
                        user_filter = filter_workout_db()
                        #Reassign conditons, parameters
                        conditions, parameters = filter_for_query(user_filter)
                        query = base_query + " WHERE " + " AND ".join(conditions)
                try:
                    #Run query
                    with sqlite3.connect("workout_selection.db") as connection:
                        cursor = connection.cursor()
                        #Using the query complete with user selected filter categories, search with user-selected values (i.e., parameters)
                        cursor.execute(query, parameters)
                        results = cursor.fetchall()
                except Exception as e:
                    print("Error: ", e)
                    return None

                if not results:
                    print("No workouts fit your criteria. Select filters again.")
                    continue

                #Display all query results
                print("Here are the search results: \n")
                for row in results:
                    print (row, "\n")

                #User selects one of the exercises
                while True:
                    try:
                        selected_workout = input("Select a workout to add to your log by entering the ID# here: ").strip()
                        if selected_workout.lower() in ["quit", ""]:
                            return None
                        else:
                            return int(selected_workout)
                        break
                    except ValueError:
                        print("Please enter a valid ID number for the workout you are selecting or type 'quit'")

            #If user types something besides y/yes when asked to select workout, exit
            else:
                return None
        except KeyboardInterrupt:
            print("\nExiting without saving...\n")
            return None


#_______________________________________________Select workout from user's database______________________________________________#
def select_custom_workout(username):
    while True:
        try:
            answer = input("Do you want to select an previously used exercise from your own log? Y/N ").lower()
            if answer in ["y", "yes"]:
                user_filter = filter_user_log(username)
                if user_filter == None:
                    return None
                #Query database based on filters user selected
                base_query = "SELECT id, name, category, equipment, primary_muscles FROM user_log WHERE username = ?"
                conditions, parameters = filter_for_query(user_filter)
                #Add username at beginning of parameters list
                parameters.insert(0, username)

                if conditions:
                    #If there are any filters selected, the base query will be updated with all items in conditions list (joined by AND)
                    query = base_query + " AND " + " AND ".join(conditions)
                else:
                    query = base_query
                try:
                    #Run query
                    with sqlite3.connect("user_log.db") as connection:
                        cursor = connection.cursor()
                        #Using the query complete with user selected filter categories, search with user-selected values (parameters)
                        cursor.execute(query, parameters)
                        results = cursor.fetchall()
                except Exception as e:
                    print("Error: ", e)
                    return None

                if not results:
                    print ("No workouts found with those filters")
                    continue
                else:
                    #Display all results
                    print("Here are the search results: \n")
                    for row in results:
                        print (row, "\n")

                #User selects one of the exercises
                while True:
                    try:
                        selected_workout = input("Select a workout to add to your log by entering the ID# here: ").strip()
                        if selected_workout.lower() in ["quit", ""]:
                            return None
                        else:
                            return int(selected_workout)
                    except ValueError:
                        print("Please enter a valid ID number for the workout you are selecting or type 'quit'")

            #If user types something besides y/yes when asked to select workout, exit
            else:
                return None
        except KeyboardInterrupt:
            print("\nExiting without saving...\n")
            return None
#--------------------------------------------------------------------------------------------------------------------------Section 2 End#




#Filters for querying larger workout and user log databases
#Section 3------------------------------------------------------------------------------------------------------------------------------#

#____________________________________________Create filter for larger workout database___________________________________________#
def filter_workout_db():
    #Current filter options (can be changed later on)
    filter_options = ["name", "category", "level", "equipment"]
    #User selects which filters they want to use
    criteria = input(f"What do you want to filter exercises by? {filter_options} - choose one or more, separated by ',': ").strip().lower()
    #Create a dictionary containing filters user chose so values can be assigned to each column/key below
    user_filter = {}
    #Map each filter chosen as stripped string
    selected_keys = [item.strip() for item in criteria.split(",")]
    #Currently user can only assign one value for each filter
    if "quit" in selected_keys:
        return None
    if "name" in selected_keys:
        name_value = input("name of exercise: (if you're not sure of the name, leave blank): ").strip()
        if name_value.lower() != "quit":
            user_filter["name"] = name_value
        else:
            return None
    if "category" in selected_keys:
        category_value = input("category (choose one: strength or cardio): ").strip()
        if category_value.lower() != "quit":
             user_filter["category"] = category_value
        else:
            return None
    if "level" in selected_keys:
        level_value = input("level (choose one: beginner, intermediate, expert): ").strip()
        if level_value.lower() != "quit":
            user_filter["level"] = level_value
        else:
            return None
    if "equipment" in selected_keys:
        #Select unique equipment values from database and display in ascending alphabetical order (ignore empty entries)
        with sqlite3.connect("workout_selection.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
            SELECT DISTINCT equipment FROM workout_selection WHERE equipment !=""
            ORDER BY equipment ASC
                           """)
            #Fetchall returns a list of tuples, with the first entry of each row containing the value, so select first of the list
            equipment_list = [row[0] for row in cursor.fetchall()]
        print("Equipment options: ", ", ".join(equipment_list))
        equipment_value = input("equipment (choose one option from above; otherwise leave blank): ").strip()
        if equipment_value.lower() != "quit":
            user_filter["equipment"] = equipment_value
        else:
            return None
    return user_filter


#__________________________________________________Create filter for user log____________________________________________________#
def filter_user_log(username):
    filter_options = ["name", "category", "equipment"]
    criteria = input(f"What do you want to filter exercises by? {filter_options} - choose one or more, separated by ',': ")
    user_filter = {}
    selected_keys = [item.strip() for item in criteria.lower().split(",")]
    if "quit" in selected_keys:
        return None
    if "name" in selected_keys:
        name_value = input("name of exercise: (if you're not sure of the name, leave blank): ").strip()
        if name_value.lower() != "quit":
            user_filter["name"] = name_value
        else:
            return None
    if "category" in selected_keys:
        category_value = input("category (choose one: strength, cardio, HIIT, yoga): ").strip()
        if category_value.lower() != "quit":
             user_filter["category"] = category_value
        else:
            return None
    if "equipment" in selected_keys:
        with sqlite3.connect("user_log.db") as connection:
            cursor = connection.cursor()
            cursor.execute("""
            SELECT DISTINCT equipment FROM user_log WHERE equipment !="" AND username = ?
            ORDER BY equipment ASC
                           """, (username, ))
            equipment_list = [row[0] for row in cursor.fetchall()]

        print("Equipment options: ", ", ".join(equipment_list))
        equipment_value = input("equipment (choose one option from above; otherwise leave blank): ").strip()
        if equipment_value.lower() != "quit":
            user_filter["equipment"] = equipment_value
        else:
            return None
    return user_filter


#______________________________________Split user criteria into filter categories and query values ______________________________#
#user_filter parameter will take returned value from filter_user_log or filter_workout_db
def filter_for_query(user_filter):
    #Conditions list will contain list of user selected filters
    conditions = []
    #Parameters will contain list of values user selected for filters
    parameters = []

    for item, value in user_filter.items():
        #Add each filter category user chose to the conditions list (plus LIKE to allow for variations in user's parameter entries), attached to placeholder ? (so we don't put user value directly into query)
        conditions.append(f"{item} LIKE ?")
        #The user's query values will be stored in parameters list (use wildcards to allow for variations in how user enters values)
        parameters.append(f"%{value}%")
    return conditions, parameters

#--------------------------------------------------------------------------------------------------------------------------Section 3 End#
