import sqlite3
import sys

#Create new user profile or retrieve existing user profile

#Create user profile database if doesn't exit
#Section 1-------------------------------------------------------------------------------------------------------------------------#
def create_user_profile_db():
    with sqlite3.connect("user_profile.db") as connection:
        cursor = connection.cursor()
        #Create table of profiles if doesn't exist; create id for each entry that autoincrements
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            age INTEGER,
            sex TEXT,
            height INTEGER,
            weight INTEGER,
            bmi FLOAT
            )""")
#---------------------------------------------------------------------------------------------------------------------Section 1 End#



#Get existing or create new user profile
#Section 2-------------------------------------------------------------------------------------------------------------------------#

#____________________________________Retrieve existing profile or ask to create new one_________________________#
#This function is currently used in main program (project.py) to manage user profile retrieval and creation
def get_profile():
    while True:
        try:
            #Attempt to retrieve existing profile by asking for unique username
            answer = input("Do you already have a user profile? Y/N: ").strip().lower()
            if answer in ["y", "yes"]:
                while True:
                    username = input("What's your username? ").strip()
                    #give user chance to exit
                    if username == "quit":
                        print("\nExiting")
                        return None

                    #Select unique username value from database
                    try:
                        with sqlite3.connect("user_profile.db") as connection:
                            cursor = connection.cursor()
                            cursor.execute("""
                                SELECT username, age, sex, height, weight FROM user_profile
                                WHERE username = ?
                            """, (username,)) #need (username,) to return a tuple - can't use (username) since this will get interpreted as as string
                            user = cursor.fetchone()

                        #if username exists in database, confirm with user that it is correct profile
                        if user != None:
                            confirm_answer = input(f"Found your profile: {user[0]} | age: {user[1]} | sex: {user[2]} | height: {user[3]} | weight: {user[4]} \nIs this you? \n").strip().lower()
                            if confirm_answer in ["y", "yes"]:
                                return user[0]
                            #If profile is not user's, they can either enter a new profile or search again
                            else:
                                create_new_answer = input("Do you want to create a new profile? Y/N ").strip().lower()
                                if create_new_answer in ["y", "yes"]:
                                    return create_user_profile(*get_inputs())
                                else:
                                    retry_answer = input("Do you want to try to search for a name again? Y/N ").strip().lower()
                                    if retry_answer in ["y", "yes"]:
                                        continue
                                    else:
                                        print("\nNo user profile retrieved or created. Exiting...\n")
                                        return None
                        #If username is not in database, user can search again, or create new profile
                        else:
                            retry_answer = input("No such username found, try again? Y/N ").strip().lower()
                            if retry_answer not in ["y", "yes"]:
                                create_new_answer = input("Do you want to create a new profile? Y/N ").strip().lower()
                                if create_new_answer in ["y", "yes"]:
                                    return create_user_profile(*get_inputs())
                                else:
                                    print("\nNo user profile retrieved or created. Exiting...\n")
                                    return None
                            #If user opts to search again, restart loop
                            else:
                                continue
            #If user types quit
            elif answer == "quit":
                print("\nExiting...")
                return None

            else:
                answer_new = input("Do you want to make a new profile? Y/N ").strip().lower()
                if answer_new in ["y", "yes"]:
                    #Run function to add user to user_profile.db and return username
                    username = create_user_profile(*get_inputs())
                else:
                    print("\nExiting...")
                    return None
                if not username:
                    continue
                else:
                    return username

        #Allow user to exit with CTRL+C
        except KeyboardInterrupt:
            print(f"\nExiting...\n")
            return None


#__________________________________________Obtain inputs for new profile________________________________________#
#Obtain new user inputs for creating profile. Function called in create_new_profile
def get_inputs():
    print("\nLet's create a new profile with a unique username!\n")
    try:
        while True:
            try:
                username = input("Name: ")
                if not username or username.strip() == "":
                    raise ValueError()
                break
            except ValueError:
                print("Please enter a name or username")
        while True:
            try:
                age = int(input("Age: "))
                if age<18 or age>80 or not age:
                    raise ValueError()
                break
            except ValueError:
                print("Please enter a valid age in years. Must be between 18 and 80 to use this program.")
        while True:
            try:
                sex = input("Sex (m/f/other): ").lower()
                if sex not in ["f", "m", "other"]:
                    raise ValueError()
                break
            except ValueError:
                print("Please enter 'f', 'm', or 'other'")
        while True:
            try:
                height = int(input("Height in inches: "))
                if height<36 or height>84:
                    raise ValueError()
                break
            except ValueError:
                print("Please enter a height in inches between 36 and 84")
        while True:
            try:
                weight = int(input("Weight (lbs): "))
                if not weight or weight<0:
                    raise ValueError()
                break
            except ValueError:
                print("Please enter a valid number for your weight in pounds")

        bmi = weight/(height**2) * 703
        if bmi<18.4 or bmi>45:
            print("Please consult with your doctor before using any excercise program")
            sys.exit()
    except KeyboardInterrupt:
        sys.exit("\nExiting without saving..")
    return username, age, sex, height, weight, bmi


#____________________________________________Create new user profile____________________________________________#
#Insert new profile entry into user profile log. Arguments are taken from function get_inputs function.
#Currently this function is called in get_profile
def create_user_profile(username, age, sex, height, weight, bmi):
    try:
        with sqlite3.connect("user_profile.db") as connection:
            cursor = connection.cursor()
            #Enter new profile in database
            cursor.execute("""
                INSERT INTO user_profile (username, age, sex, height, weight, bmi)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (username, age, sex, height, weight, bmi))

        print(f"Profile for {username} was created!")
        return username

    #If can't enter profile (if username isn't unique), use custom IntegrityError
    except sqlite3.IntegrityError:
        print(f"Error: The username '{username}' is taken. Please choose another username.")
        return None

#---------------------------------------------------------------------------------------------------------------------Section 2 End#
