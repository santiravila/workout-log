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

    routines = manager.routines
    if not routines:
        print("No saved Routines")
        return
    
    print("Choose from one of these routines: ")
    print_routines(routines)
    
    routine_name = input("Routine name: ")
    routine = manager.get_routine(routine_name)
    if not routine:
        print("Not an existing routine")
        return
    
    exercise_data = get_reps_for_session(routine)
    manager.create_session(routine_name, exercise_data)


def get_reps_for_session(routine):
    exercises = routine.exercises
    exercise_data = []

    for exercise in exercises:
        session_reps = []
        print(exercise.name)
        for i in range(1, exercise.sets + 1):
            session_reps.append(int(input(f"Reps for set {i}: ")))
        exercise_data.append(
            {
                "name": exercise.name,
                "sets": exercise.sets,
                "weight": exercise.weight,
                "reps": session_reps,
            }
        )
    return exercise_data


def print_routines(routines):
    for routine in routines:
        print(f"{routine.id} | {routine.name}")


def consult_log():
    print("\n=================== EXISTING SESSIONS ===================\n")
    routines = manager.sessions
    if not routines:
        print("No saved Sessions")
    else:
        for routine in routines:
            routine_exercises = routine.exercises
            print(routine)
            for exercise in routine_exercises:
                print(exercise)
            print()


def consult_routines():
    print("\n=================== EXISTING ROUTINES ===================\n")
    routines = manager.routines
    if not routines:
        print("No saved Routines")
    else:
        for routine in routines:
            print(routine)
            routine_exercises = routine.exercises
            for exercise in routine_exercises:
                print(exercise)
            print()
