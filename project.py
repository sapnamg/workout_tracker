import sys
from user_profile import create_user_profile_db, get_profile
from workout_selector import fetch_workout_database, select_workout, select_custom_workout
from user_log import create_user_log, custom_workout, add_workout, edit_workout, delete_workout
from workout_stats import display_user_log

#Workout Tracker - Main file

#_________________________________________________________________Main Program_____________________________________________________________#
def main():
    try:
        #Introduction and basic instructions
        print("""
          Welcome to your Workout Tracker! With a unique username, you can log your workouts and keep track of your progress.
          You can get new ideas for workouts from a list of over 800 workouts, or just add your own custom ones.
          Get started by entering accessing your profile or creating one! You can quit any time by pressing CTRL+C (or 'quit' when prompted)
          Enjoy!
          """)

        #Ensure user profile, user log, and workout database exists (otherwise will be created)
        create_user_profile_db()
        create_user_log()
        fetch_workout_database()

        #Ask user for a previous profile name or to create new one
        username = get_profile()

        if not username:
            print("\nNo user profile retrieved or created. Exiting...\n")
            sys.exit()

        else:
            #Loop through adding workout and displaying log until user wants to stop
            while True:
                add_answer = input("Do you want to add to your log? Y/N ").strip().lower()
                if add_answer in ["y","yes"]:
                    add_workout_loop(username)
                else:
                    break

                display_answer = input("Do you want to see your complete log? Y/N ").strip().lower()
                if display_answer in ["y","yes"]:
                    display_user_log(username)
                else:
                    break

            #Give user option to edit, delete, or add workout, or display log again before exiting
            while True:
                user_action = input("""
Type 'edit' if you want to edit a log entry,
'delete' if you want to delete a log entry,
'add' if you want to add another workout,
'display' if you want to see your log,
and 'quit' to quit the program:
""").strip().lower()
                if user_action == "quit":
                    print("Thanks for using this workout log! Goodbye!")
                    sys.exit()
                elif user_action == "edit":
                    edit_workout(username)
                elif user_action == "delete":
                    delete_workout(username)
                elif user_action == "add":
                    add_workout_loop(username)
                elif user_action == "display":
                    display_user_log(username)

    except KeyboardInterrupt:
        print("\nExiting...\n")
        sys.exit()




#__________________________________________________Loop through all options to add workout_________________________________________________#
def add_workout_loop(username):
    #Set all variables to None (need to reset each time this loop is called to maintain logic for conditions below)
    workout_id = None
    user_workout_id = None
    new_custom_id = None

    workout_id = select_workout()
    if workout_id == None:
        user_workout_id = select_custom_workout(username)
        if user_workout_id == None:
            new_custom_id = custom_workout(username)
            if new_custom_id == None:
                print("\nNo workout selected or added\n")
            else:
                add_workout(username, workout_id, user_workout_id, new_custom_id)
        else:
            add_workout(username, workout_id, user_workout_id, new_custom_id=None)
    else:
        add_workout(username, workout_id, user_workout_id=None, new_custom_id=None)




#____________________________________________________________Run Main Program_____________________________________________________________#
if __name__ == "__main__":
    main()
