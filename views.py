from controller import manager


def print_menu():
    print(
        "\n========================= MAIN MENU =========================\n\n"
        "1. Create new Workout Session\n"
        "2. Consult Workout Log\n"
        "3. Create a new Routine\n"
        "4. Consult Routines\n"
        "5. Exit\n"
    )


def get_user_input():
    while True:
        try:
            option = int(input("Option: "))
            return option
        except ValueError:
            pass


def create_routine():
    print("\n=================== ROUTINE CREATION ===================\n")
    
    while True:
        try:
            name = input("Name: ")
            creation = manager.start_routine_creation(name)
            break
        except ValueError as e:
            print(e)

    exercise_num = int(input("Number of exercises: "))
    for i in range(1, exercise_num + 1):
        while True:
            try:
                name = input(f"Exercise No.{i} name: ")
                sets = int(input(f"Exercise No.{i} set number: "))
                weight = float(input(f"Exercise No.{i} weight: "))
                creation.add_exercise(name, sets, weight)
                break
            except ValueError as e:
                print(e)
    
    creation.set_rest(float(input("Rest: ")))
    creation.set_tempo(input("Tempo: "))

    try:
        creation.finish()
        print("Routine created successfully")
    except ValueError as e:
        print(f"Error creating routine: {e}")


def create_session():
    print("\n=================== SESSION CREATION ===================\n")

    routines = manager.get_routines()
    if not routines:
        print("No saved routines")
        return

    print_routines(routines)

    while True:
        try:
            routine_index = int(input("Routine index: "))
            routine = manager.get_routine(routine_index)
            creation = manager.start_session_creation(routine)
            break
        except ValueError as e:
            print(e)

    for exercise in routine.exercises:
        print(f"Fill reps for each set of {exercise.name}")
        for set in range(exercise.sets):
            while True:
                try:
                    reps = int(input(f"Reps for set {set + 1}: "))
                    creation.add_reps(exercise, set, reps)
                    break
                except ValueError as e:
                    print(e)
                    
    creation.finish()


def print_routines(routines):
    for routine in routines:
        print(f"{routine.id} | {routine.name}")


def consult_log():
    print("\n=================== EXISTING SESSIONS ===================\n")

    print("1 | Show all logged sessions in chronological order")
    print("2 | Filter sessions by routine")
    print("3 | Return to main menu\n")
    
    option = consult_log_choice()
    if option == 1:
        print_sessions()
    elif option == 2:
        print_filtered_sessions()
    elif option == 3:
        return


def consult_log_choice():
    while True:
        try:
            option = int(input("Option: "))
            if option < 0 or option > 3:
                pass
            break
        except ValueError:
            pass

    return option
    

def print_sessions():
    sessions = manager.get_sessions()
    if not sessions:
        print("\nNo saved Sessions")
        return

    print()
    for session in sessions:
        session_exercises = session.exercises
        print(session)
        for exercise in session_exercises:
            print(exercise)
        print()


def print_filtered_sessions():
    print("Select a routine: ")
    routines = manager.get_routines()

    print_routines(routines)

    while True:
        try:
            routine_index = int(input("Routine index: "))
            routine = manager.get_routine(routine_index)
            break
        except ValueError as e:
            print(e)

    sessions = manager.get_sessions()
    
    filtered_sessions = [
        session 
        for session in sessions 
        if session.routine_name == routine.name
    ]

    if not filtered_sessions:
        print(f"\nNo existing sessions based on routine: {routine.name}")
        return
    
    print()
    for filtered in filtered_sessions:
        print(filtered)
        for exercise in filtered.exercises:
            print(exercise)
        print()


def consult_routines():
    print("\n=================== EXISTING ROUTINES ===================\n")

    routines = manager.routines
    if not routines:
        print("No saved Routines")
        return
    
    for routine in routines:
        print(routine)
        routine_exercises = routine.exercises
        for exercise in routine_exercises:
            print(exercise)
        print()
