from models import AppManager


manager = AppManager()


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
    print("\n=================== NEW ROUTINE CREATION ===================\n")
    routine_name = input("Name: ")
    exercise_num = int(input("Number of exercises: "))
    exercise_data = []  # NO EDD EN VIEW

    # Routine Serialization
    for i in range(1, exercise_num + 1):
        exercise_name = input(f"Exercise No.{i} name: ")
        set_num = int(input(f"Exercise No.{i} set number: "))
        weight = float(input(f"Exercise No.{i} weight: "))
        exercise_data.append({"name": exercise_name, "sets": set_num, "weight": weight})
    rest = float(input("Rest: "))
    tempo = input("Tempo: ")

    manager.create_routine(routine_name, rest, tempo, exercise_data)


def create_session():
    print("\n=================== NEW SESSION CREATION ===================\n")
    routines = manager.routines
    if not routines:
        print("No saved Routines")
    else:
        print("Choose from one of these routines: ")
        print_routines(routines)
        routine_name = input("Routine name: ")
        routine = manager.get_routine(routine_name)
        if not routine:
            print("Not an existing routine")
        else:
            exercises = routine.exercises
            exercise_data = []

            for i, exercise in enumerate(exercises):
                session_reps = []
                print(exercise.name)
                for j in range(1, exercise.sets + 1):
                    session_reps.append(int(input(f"Reps for set {j}: ")))
                exercise_data.append(
                    {
                        "name": exercise.name,
                        "sets": exercise.sets,
                        "weight": exercise.weight,
                        "reps": session_reps,
                    }
                )

            manager.create_session(routine_name, exercise_data)


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
