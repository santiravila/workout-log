from classes import Routine, Exercise, Session
from datetime import date
from copy import deepcopy

def main():
    routines = []
    sessions = []
    while True:
        print(
        "\n========================= MAIN MENU =========================\n\n" \
        "1. Create new Workout Session\n" \
        "2. Consult Workout Log\n" \
        "3. Create a new Routine\n" \
        "4. Consult Routines\n" \
        "5. Exit\n" \
        )
        try:
            option = int(input("Option: "))
        except ValueError:
            pass
        match option:
            case 1:
                if not routines:
                    print("\nYou have no saved Routines, please create one")
                else:
                    sessions.append(create_session(routines))
            case 2:
                if not sessions:
                    print("\nNo saved Sessions")
                else:
                    print_sessions(sessions)
            case 3:
                routines.append(create_routine())
            case 4:
                if not routines:
                    print("\nNo saved Routines")
                else:
                    print_routines(routines)
                continue
            case 5:
                break # Exit
            case _:
                continue   
            

def create_routine() -> Routine:
    if hasattr(create_routine, "Routine_ID"):
        create_routine.Routine_ID += 1
    else:
        setattr(create_routine, "Routine_ID", 1)

    print("\n=================== NEW ROUTINE CREATION ===================\n")
    routine_name = input("Name: ")
    exercise_num = int(input("Number of exercises: "))
    exercise_list = []
    for i in range(1, exercise_num+1):
        exercise_name = input(f"Exercise No.{i} name: ")
        set_num = int(input(f"Exercise No.{i} set number: "))
        weight = float(input(f"Exercise No.{i} weight: "))
        exercise_list.append(Exercise(exercise_name, set_num, weight))
    rest = float(input("Rest: "))
    tempo = input("Tempo: ")
    routine = Routine(create_routine.Routine_ID, routine_name, rest, tempo, exercise_list)
    return routine


def create_session(routines: list[Routine]):
    if hasattr(create_session, "Session_ID"):
        create_session.Session_ID += 1
    else:
        setattr(create_session, "Session_ID", 1)

    print("Choose from one of these routines: ")
    for routine in routines:
        print(f"{routine.id} | {routine.name}")

    found_routine = False
    option = int(input("Routine number: "))
    for routine in routines:
        if option == routine.id:
            choosen_routine = deepcopy(routine)
            found_routine = True

    if found_routine:
        session = Session(id=create_session.Session_ID, routine_name=choosen_routine.name, date=date.today(), exercises=choosen_routine.exercises)
        exercises = session.exercises

        for i, exercise in enumerate(exercises):
            session_reps = []
            print(exercise.name)
            for j in range(1, exercise.sets+1):
                session_reps.append(int(input(f"Reps for set {j}: ")))
            session.exercises[i].reps = session_reps
        return session 
    return None


def print_routines(routines: list[Routine]):
    print("\n=================== EXISTING ROUTINES ===================\n")
    for routine in routines:
        routine_exercises = routine.get_exercises()
        print(routine)
        for exercise in routine_exercises:
            print(exercise)
        print()
    

def print_sessions(sessions: list[Session]): 
    print("\n=================== EXISTING SESSIONS ===================\n")
    for session in sessions:
        print(session)
        session_exercises = session.exercises
        for exercise in session_exercises:
            print(exercise)
        print()


if __name__ == "__main__":
    main()
