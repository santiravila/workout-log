from controller import manager
import inflect
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.tree import Tree


p = inflect.engine()
console = Console()


def ordinal(n: int) -> str:
    return p.ordinal(n) # type: ignore[arg-type]


def print_menu():
    menu_text = """
    1. Create new Workout Session
    2. Consult Workout Log
    3. Create a new Routine
    4. Consult Routines
    5. Exit
    """
    menu = Align.center(menu_text)

    console.print(
        Panel(
            menu,
            title="MAIN MENU",
            subtitle="Select an option",
            border_style="cyan",
            padding=(1, 2),
        )
    )


def get_user_input():
    while True:
        try:
            option = int(input("Option: "))
            return option
        except ValueError:
            pass


def create_routine():
    panel = Panel(
        "asa",
        title="SESSION CREATION"
    )
    
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
                name = input(f"{ordinal(i)} Exercise name: ")
                sets = int(input(f"{ordinal(i)}Exercise set number: "))
                weight = float(input(f"{ordinal(i)} Exercise weight: "))
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
                    reps = int(input(f"Reps for {ordinal(set + 1)} set: "))
                    creation.add_reps(exercise, set, reps)
                    break
                except ValueError as e:
                    print(e)
                    
    creation.finish()


def print_routines(routines):
    for routine in routines:
        print(f"{routine.id} | {routine.name}")


def consult_log():
    menu_text = """
        1. Display saved sessions
        2. Filter sessions by routine
        3. Return to main menu
    """

    menu = Align.center(menu_text)

    console.print(
        Panel(
            menu,
            title="SAVED SESSIONS",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    
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
        console.print(
            Panel(
                "No saved sessions",
                title="SAVED SESSIONS",
                border_style="red",
            )
        )
        return
    
    tree = Tree("Sessions", guide_style="bold cyan")
    
    for session in sessions:
        session_node = tree.add(f"[bold]{session}[/bold]")
        for exercise in session.exercises:
            session_node.add(f"{str(exercise)}")

    console.print(
        Panel(
            tree,
            title="SAVED SESSIONS",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    exit = input("Return to main menu")
    if exit:
        return


def print_filtered_sessions():
    routines = manager.get_routines()
    if not routines:
        console.print(
            Panel(
                "No saved routines",
                title="Routines",
                border_style="red",
            )
        )
        return

    routines_tree = Tree("Available Routines", guide_style="bold cyan")
    for i, routine in enumerate(routines, start=1):
        routines_tree.add(f"[bold]{i}[/bold] · {routine.name}")
    
    console.print(Panel(routines_tree, border_style="cyan"))

    while True:
        try:
            routine_index = int(console.input("[bold cyan]Routine index:[/] "))
            routine = manager.get_routine(routine_index)
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    sessions = manager.get_sessions()
    
    filtered_sessions = [
        session 
        for session in sessions 
        if session.routine_name == routine.name
    ]

    if not filtered_sessions:
        console.print(
            Panel(
                f"No existing sessions based on routine: [bold]{routine.name}[/bold]",
                title="Sessions",
                border_style="yellow",
            )
        )
        return
    
    sessions_tree = Tree(
        f"Sessions for [bold]{routine.name}[/bold]",
        guide_style="bold green",
    )
    
    for session in filtered_sessions:
        session_node = sessions_tree.add(f"[bold]{session}[/bold]")

        for exercise in session.exercises:
            session_node.add(str(exercise))

    console.print(
        Panel(
            sessions_tree,
            title="Workout History",
            border_style="green",
            padding=(1, 2),
        )
    )


def consult_routines(routines):
    if not routines:
        console.print(
            Panel(
                "No saved routines",
                title="Saved Routines",
                border_style="red",
            )
        )
        return
    
    tree = Tree("Routines", guide_style="bold cyan")
    
    for routine in routines:
        routine_node = tree.add(f"[bold]{routine}[/bold]")

        for exercise in routine.exercises:
            routine_node.add(str(exercise))

    console.print(
        Panel(
            tree,
            title="SAVED ROUTINES",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    exit = input("Return to main menu")
    if exit:
        return