import sqlite3
import datetime

#User log database creation and manipulation.
#Includes function to create custom exercise (as it is saved in user log)

#User workout log database creation
#Section 1------------------------------------------------------------------------------------------------------------------------------#
def create_user_log():
    with sqlite3.connect("user_log.db") as connection:
        cursor = connection.cursor()

        #Create table of workouts tied to username; create id for each entry that autoincrements
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_log (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       username TEXT,
                       name TEXT NOT NULL,
                       category TEXT,
                       date TEXT,
                       time TEXT,
                       duration INTEGER,
                       distance INTEGER,
                       weight INTEGER,
                       reps INTEGER,
                       equipment TEXT,
                       primary_muscles TEXT,
                       secondary_muscles TEXT,
                       instructions TEXT,
                       notes TEXT
                       )
        """)
#--------------------------------------------------------------------------------------------------------------------------Section 1 End#




#Obtain information required for exercise to be added to log
#Section 2------------------------------------------------------------------------------------------------------------------------------#
#_________________________________________________Create custom workout_________________________________________________________#
#Let user define custom exercise, and then add to user_log (without date) so it can be retrieved later with an id#. Need username as parameter so it's only added for this user.
def custom_workout(username):
    try:
        answer = input("Do you want to create your own workout manually? Y/N ").lower()
        #User can exit here by not typing y/yes
        if answer not in ["y","yes"]:
            return None
        else:
            #Create name (required)
            while True:
                name = input("Workout name: ").strip()
                if not name:
                    print("Please enter a workout name, or type 'quit'")
                elif name.lower() == "quit":
                    return None
                else:
                    break
            #Create category (optional)
            while True:
                category = input("Type of workout (optional) (strength, cardio, HIIT, yoga, other): ").strip().lower()
                #Can leave empty or enter from below set only
                if category in ["strength", "cardio", "hiit", "yoga", "other", ""]:
                    break
                elif category == "quit":
                    return None
                else:
                    print("please enter workout type from: strenght, cardio, HIIT, yoga, or other")

            #Other optional fields
            equipment = input("Equipment (optional): ").strip().lower()
            if equipment == "quit":
                return None
            primary_muscles = input("Primary muscle group (optional): ").strip().lower()
            if primary_muscles == "quit":
                return None
            secondary_muscles = input("Secondary muscle group (optional): ").strip().lower()
            if secondary_muscles == "quit":
                return None
            instructions = input("Instructions (free-text):\n").strip().lower()
            if instructions == "quit":
                return None

            #Enter this workout in the user_log (without date) and then obtain its id
            with sqlite3.connect("user_log.db") as connection:
                cursor = connection.cursor()
                #Add workout to user's log
                cursor.execute("""
                    INSERT INTO user_log (username, name, category, equipment, primary_muscles, secondary_muscles, instructions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (username, name, category, equipment, primary_muscles, secondary_muscles, instructions))

                #select the workout and obtain the id
                cursor.execute("""
                    SELECT id from user_log WHERE username = ? AND name = ?
                """, (username, name))
                new_custom_id = cursor.fetchone()[0]
            #return id# to be used later to retrieve workout information (in get_workout_info)
            return new_custom_id

    except KeyboardInterrupt:
        print("\nExiting...\n")
        return None


#______________________________________________Retrieve base information about chosen workout____________________________________#
#Get basic workout information in dictionary format (to be used with additional workout details in add_workout function)
def get_workout_info(workout_id, user_workout_id, new_custom_id):
    if workout_id:
        with sqlite3.connect("workout_selection.db") as connection:
            #Retun items as rows so can make dict from them
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
            SELECT id, name, category, primary_muscles, secondary_muscles, instructions FROM workout_selection WHERE id = ?
                           """, (workout_id,))
            workout_selected = cursor.fetchone()
            return dict(workout_selected)
    elif user_workout_id:
        with sqlite3.connect("user_log.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
            SELECT id, name, category, primary_muscles, secondary_muscles, instructions FROM user_log WHERE id = ?
                           """, (user_workout_id,))
            workout_selected = cursor.fetchone()
            return dict(workout_selected)
    elif new_custom_id:
        with sqlite3.connect("user_log.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            cursor.execute("""
            SELECT id, name, category, primary_muscles, secondary_muscles, instructions FROM user_log WHERE id = ?
                           """, (new_custom_id,))
            workout_selected = cursor.fetchone()
            return dict(workout_selected)
    else:
        return None


#______________________________________________Obtain details for current workout entry__________________________________________#
#User prompted for current workout details (date, duration, reps, etc.). Returns dictionary of details to be used in add_workout function.
def current_workout_details():
    print("Enter the details of your workout for logging")
    try:
        #Date is required
        while True:
            date = input("Date (MM/DD/YYYY): ").strip()
            if date == "" or not date:
                print ("A date is required.")
                return None
            try:
                date_object = datetime.datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
                break
            except ValueError:
                print("Incorrect date format")

        #Other optional fields
        time = None
        duration = None
        distance = None
        weight = None
        reps = None

        #Input values for optional fields
        while True:
            time = input("Time of day (optional) (HH:MM 24-hour format): ").strip()
            if time == "":
                break
            try:
                time_object = datetime.datetime.strptime(time, "%H:%M").time()
                break
            except ValueError:
                print("Incorrect time format")

        while True:
            duration = input("Duration (optional) (in minutes): ").strip()
            if duration == "":
                break
            try:
                duration = int(duration)
                break
            except ValueError:
                print("Incorrect duration format, enter numbers for duration in total minutes")

        while True:
            distance = input("Distance (optional) in miles: ").strip()
            if distance == "":
                break
            try:
                distance = float(distance)
                break
            except ValueError:
                print("Enter distance as a number (of miles)")

        while True:
            weight = input("Weight (optional) in lbs: ").strip()
            if weight == "":
                break
            try:
                weight = int(weight)
                break
            except ValueError:
                print("Enter weight as a number (of pounds)")

        while True:
            reps = input("# of Reps (optional): ").strip()
            if reps == "":
                break
            try:
                reps = int(reps)
                break
            except ValueError:
                print("Enter an integer for reps")

        notes = input("Notes (optional free-text):\n").strip()

        return {
            "date" : date,
            "time" : time,
            "duration" : duration,
            "distance" : distance,
            "weight" : weight,
            "reps" : reps,
            "notes" : notes
        }

    except KeyboardInterrupt:
        print("\nExiting without saving...\n")
        return None


#--------------------------------------------------------------------------------------------------------------------------Section 2 End#




#Database manipulation functions
#Section 3------------------------------------------------------------------------------------------------------------------------------#

#_________________________________________________Add a workout to log__________________________________________________________#
#Uses id from either selected workout or custom workout, and associates with user's profile
def add_workout(username, workout_id, user_workout_id, new_custom_id):
    answer = input("Do you want to add this workout to your log? Y/N: ").strip().lower()
    if answer in ["y", "yes"]:
        #Returns dictionary of workout info from workout selected or created
        workout_info = get_workout_info(workout_id, user_workout_id, new_custom_id)
        if not workout_info:
            print("There was an error. The workout can't be added; try again.")
            return None
        while True:
            workout_details = current_workout_details()
            if not workout_details:
                entry_answer = input("Not enough workout details obtained. Do you want to quit this entry? Y/N ").strip().lower()
                if entry_answer in ["y", "yes"]:
                    print("The workout wasn't added.")
                    return None
                else:
                    continue
            else:
                log_workout(username, workout_info, workout_details)
                print("Workout added to your log!")
                break


#___________________________________Function to insert entry in log (used in add_workout function)______________________________#
def log_workout(username, workout_info, workout_details):
    with sqlite3.connect("user_log.db") as connection:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO user_log (
                            username, name, category, date, time, duration, distance, weight, reps, equipment, primary_muscles, secondary_muscles, instructions, notes)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            #the below tuple will be inserted into respective columns (where ? is currently placeholder)
                            (
                                username,
                                workout_info.get("name"),
                                workout_info.get("category"),
                                workout_details.get("date"),
                                workout_details.get("time"),
                                workout_details.get("duration"),
                                workout_details.get("distance"),
                                workout_details.get("weight"),
                                workout_details.get("reps"),
                                workout_info.get("equipment"),
                                workout_info.get("primary_muscles"),
                                workout_info.get("secondary_muscles"),
                                workout_info.get("instructions"),
                                workout_details.get("notes")
                            )
                            )
    print(f"Entered {workout_info["name"]} in your log!")


#_________________________________________________Edit entry in log_____________________________________________________________#
#Need username as parameter to allow selection from user's database only
def edit_workout(username):
    while True:
        try:
            #Use ID of workout to select it. User is given option to display their log in main program to see ID
            id_selection = input("Select the ID of the row you want to edit: ").strip()
            if id_selection.lower() == "quit":
                print("Cancelling action...")
                return None
            #if ID is not a number it will raise ValueError (handled below)
            id_selection = int(id_selection)
            #Validate that ID exists for this username, and get name of associated exercise
            with sqlite3.connect("user_log.db") as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()

                #Get name for workout if id belongs to username and exists
                cursor.execute("""
                    SELECT name FROM user_log WHERE username = ? AND id = ?
                """, (username, id_selection))
                #store item from user's log
                user_log_entry = cursor.fetchone()

                #check that entry (id and name) exists:
                if user_log_entry:
                    id_name = user_log_entry["name"]
                    break
                else:
                    raise ValueError("ID not found in your log")
        except ValueError:
            print("Please type a valid ID number or type 'quit' ")

    #User selects column they want to change
    #Can later adapt accepted columns to expand functionality but then must also addend below section obtaining validating new entry for given column
    accepted_columns = ["name", "category", "date", "duration", "distance", "weight", "reps"]
    while True:
        column_selection = input(f"What column do you want to edit: {', '.join(accepted_columns)}: ").strip().lower()
        if column_selection == "quit":
            print("Cancelling action...")
            return None
        if column_selection in accepted_columns:
            break
        else:
            print("Please select valid column from choices mentioned. Try again or type quit when asked for selection.")

    #Obtain new entry from user and validate input
    while True:
        if column_selection == "name":
            new_entry = input("Workout name: ").strip()
            if not new_entry or new_entry.lower() == "quit":
                print("Cancelling action...")
                return None
            else:
                break
        elif column_selection == "category":
            new_entry = input("Type of workout (optional) (strength, cardio, HIIT, yoga, other): ").strip().lower()
            if new_entry in ["strength", "cardio", "hiit", "yoga", "other", ""]:
                break
            elif new_entry == "quit" or not new_entry:
                print("Cancelling action...")
                return None
            else:
                print("please enter workout type from: strenght, cardio, HIIT, yoga, or other")
        elif column_selection == "date":
            new_entry = input("Date (MM/DD/YYYY): ").strip()
            if new_entry == "quit" or not new_entry:
                print("Cancelling action...")
                return None
            try:
                new_entry = datetime.datetime.strptime(new_entry, "%m/%d/%Y").strftime("%Y-%m-%d")
                break
            except ValueError:
                print("Incorrect date format")
        elif column_selection == "time":
            new_entry = input("Time of day (optional) (HH:MM 24-hour format): ").strip()
            if new_entry == "quit" or not new_entry:
                print("Cancelling action...")
                return None
            try:
                new_entry = datetime.datetime.strptime(new_entry, "%H:%M").time()
                break
            except ValueError:
                print("Incorrect time format")
        elif column_selection in ["duration", "weight", "reps"]:
            new_entry = input("New entry: ").strip()
            if new_entry == "quit" or not new_entry:
                print("Cancelling action...")
                return None
            try:
                new_entry = int(new_entry)
                break
            except ValueError:
                print("Incorrect format, please enter an integer.")
        elif column_selection == "distance":
            new_entry = input("Distance (optional) in miles: ").strip()
            if new_entry == "quit" or not new_entry:
                print("Cancelling action...")
                return None
            try:
                new_entry = float(new_entry)
                break
            except ValueError:
                print("Enter distance as a number(integer or decimal) (of miles)")

    #Update user_log based on ID# and column_selection, with new entry
    with sqlite3.connect("user_log.db") as connection:
        cursor = connection.cursor()

        update_query = f"""
        UPDATE user_log
        SET {column_selection} = ?
        WHERE id = ?
        """
        cursor.execute(update_query, (new_entry, id_selection))

        if column_selection == "name":
            print(f"{column_selection.capitalize()} updated for {id_selection} to {new_entry}!")
        else:
            print(f"{column_selection.capitalize()} updated for {id_selection}: {id_name} to {new_entry}!")


#___________________________________________________Delete entry from log_______________________________________________________#
#Need username as parameter to allow selection from user's database only
def delete_workout(username):
    while True:
        try:
            id_selection = input("Select the ID of the row you want to delete: ").strip()
            if id_selection.lower() == "quit":
                print("Cancelling action...")
                return None
            id_selection = int(id_selection)
            #get list of IDs under username to check if selection is in this list
            with sqlite3.connect("user_log.db") as connection:
                connection.row_factory = sqlite3.Row
                cursor = connection.cursor()

                #get name for workout if id belongs to username and exists
                cursor.execute("""
                    SELECT name, date FROM user_log WHERE username = ? AND id = ?
                """, (username, id_selection))
                #store item from user's log
                user_log_entry = cursor.fetchone()

                #check that entry (id and name) exists:
                if user_log_entry:
                    id_name = user_log_entry["name"]
                    id_date = user_log_entry["date"]
                    break
                else:
                    raise ValueError("ID not found in your log")
        except ValueError:
            print("Please type a valid ID number or type 'quit' ")

        #confirm user wants to delete
    confirm_delete = input(f"Confirm you want to delete entry: {id_selection}: {id_name} from {id_date}: Y/N ").strip().lower()
    if confirm_delete not in ["y", "yes"]:
        print("Cancelling action...")
        return None
    else:
        #delete entry from table
        with sqlite3.connect("user_log.db") as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()
            #get name for workout if id belongs to username and exists
            cursor.execute("""
                DELETE FROM user_log
                WHERE username = ? AND id = ? AND name = ? AND date = ?
                           """, (username, id_selection, id_name, id_date))
            #store item from user's log
            connection.commit()
        print(f"Deleted entry {id_selection}: {id_name} from {id_date} from your log!")

#--------------------------------------------------------------------------------------------------------------------------Section 3 End#
