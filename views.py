from controller import manager
import inflect
import matplotlib.pyplot as plt # TEMPORARY, GO TO MODELS
import numpy as np # TEMPORARY, GO TO MODELS
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.tree import Tree


p = inflect.engine()
console = Console()


def ordinal(n: int) -> str:
    return p.ordinal(n)  # type: ignore[arg-type]


def print_menu():
    console.clear()

    menu_text = """
    1. Create new Workout Session
    2. View Workout Log
    3. Create a new Routine
    4. View Routines
    5. Create workout report
    6. Exit
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
            option = int(console.input(f"[bold cyan]Option:[/] "))
            return option
        except ValueError:
            pass


def create_routine():
    console.clear()

    console.print(
        Panel(
            "Enter the data requested below.\nFields marked are required.",
            title="[bold cyan]Routine Creation[/bold cyan]",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    # Get Routine name
    while True:
        try:
            name = console.input("[bold cyan]Name:[/] ").strip()
            creation = manager.start_routine_creation(name)
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    # Get Exercise count
    while True:
        try:
            exercise_num = int(console.input("[bold cyan]Number of exercises:[/] "))
            if exercise_num <= 0:
                raise ValueError("Must be greater than zero")
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    # Get the Exercises themselves
    for i in range(1, exercise_num + 1):
        console.print(f"[bold]{ordinal(i)} Exercise[/bold]")

        while True:
            try:
                name = console.input("  [cyan]Name:[/] ").strip()
                sets = int(console.input("  [cyan]Sets:[/] "))
                weight = float(console.input("  [cyan]Weight:[/] "))
                creation.add_exercise(name, sets, weight)
                break
            except ValueError as e:
                console.print(f"[red]{e}[/red]")

    while True:
        try:
            creation.set_rest(float(console.input("\n[bold cyan]Rest (seconds):[/] ")))
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    creation.set_tempo(console.input("[bold cyan]Tempo (optional):[/] ").strip())

    try:
        creation.finish()
        console.print(
            Panel(
                "[bold green]Routine created successfully[/bold green]",
                border_style="green",
            )
        )
    except ValueError as e:
        console.print(
            Panel(
                f"[red]Error creating routine:[/] {e}",
                border_style="red",
            )
        )

    exit = input("Return to main menu") or True
    if exit:
        return


def create_session(routines):
    console.clear()

    if not routines:
        print("No saved routines")
        return

    routines_tree = Tree("Routines")

    for i, routine in enumerate(routines, start=1):
        routines_tree.add(f"[bold]{i}[/bold] · {routine.name}")

    console.print(Panel(routines_tree, border_style="cyan", title="Routine Selection"))

    while True:
        try:
            routine_index = int(console.input("[bold cyan]Routine index:[/] "))
            routine = manager.get_routine(routine_index)
            creation = manager.start_session_creation(routine)
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    for exercise in routine.exercises:
        print(f"Fill reps for each set of {exercise.name}")
        for set in range(exercise.sets):
            while True:
                try:
                    reps = int(
                        console.input(
                            f"[bold cyan]Reps for {ordinal(set + 1)} set:[/] "
                        )
                    )
                    creation.add_reps(exercise, reps)
                    break
                except ValueError as e:
                    console.print(f"[red]{e}[/red]")

    try:
        creation.finish()
        console.print(
            Panel(
                "[bold green]Session created successfully[/bold green]",
                border_style="green",
            )
        )
    except ValueError as e:
        console.print(
            Panel(
                f"[red]Error creating session:[/] {e}",
                border_style="red",
            )
        )
    
    exit = input("Return to main menu") or True
    if exit:
        return


def print_routines(routines):
    # validate
    if not routines:
            console.print(
                Panel(
                    "No saved routines",
                    title="Routines",
                    border_style="red",
                )
            )
            return
    
    # show available routines
    routines_tree = Tree("Available Routines", guide_style="bold cyan")
    for i, routine in enumerate(routines, start=1):
        routines_tree.add(f"[bold]{i}[/bold] · {routine.name}")

    console.print(Panel(routines_tree, border_style="cyan"))


def view_log(sessions, routines):
    console.clear()

    if not sessions:
        console.print(
            Panel(
                "No saved sessions",
                title="SAVED SESSIONS",
                border_style="red",
            )
        )
        return

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

    # consult option
    while True:
        try:
            option = int(input("Option: "))
            if option < 0 or option > 3:
                pass
            break
        except ValueError:
            pass

    if option == 1:
        print_sessions(sessions=sessions)
    elif option == 2:
        # show routines
        routine_tree = Tree("Routines", guide_style="bold cyan")

        for i, routine in enumerate(routines, start=1):
            routine_tree.add(f"[bold]{i}[/bold] · {routine.name}")

        console.print(routine_tree)

        # get routine
        while True:
            try:
                routine_index = int(console.input("[bold cyan]Routine index:[/] "))
                routine = manager.get_routine(routine_index)
                break
            except ValueError as e:
                console.print(f"[red]{e}[/red]")

        try:
            filtered_sessions = filter_sessions_by_routine(sessions, routine)
        except ValueError:
            exit = input("Return to main menu") or True
            if exit:
                return
        else:
            print_sessions(filtered_sessions)
    
    elif option == 3:
        return


def print_sessions(sessions):
    console.clear()

    sessions_tree = Tree("Sessions", guide_style="bold cyan")

    for session in sessions:
        session_node = sessions_tree.add(f"[bold]{session}[/bold]")
        for exercise in session.exercises:
            session_node.add(f"{str(exercise)}")

    console.print(
        Panel(
            sessions_tree,
            title="SESSIONS",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    exit = input("Return to main menu") or True
    if exit:
        return


def filter_sessions_by_routine(sessions, routine):
    filtered_sessions = [
        session for session in sessions if session.routine_name == routine.name
    ]

    if not filtered_sessions:
        console.print(
            Panel(
                f"No existing sessions based on routine: [bold]{routine.name}[/bold]",
                title="Sessions",
                border_style="yellow",
            )
        )
        raise ValueError
    
    return filtered_sessions


def view_routines(routines):
    console.clear()

    if not routines:
        console.print(
            Panel(
                "No saved routines",
                title="Saved Routines",
                border_style="red",
            )
        )
        return

    routine_tree = Tree("Routines", guide_style="bold cyan")

    for routine in routines:
        routine_node = routine_tree.add(f"[bold]{routine}[/bold]")

        for exercise in routine.exercises:
            routine_node.add(str(exercise))

    console.print(
        Panel(
            routine_tree,
            title="SAVED ROUTINES",
            border_style="cyan",
            padding=(1, 2),
        )
    )

    exit = input("Return to main menu") or True
    if exit:
        return


def create_report(routines, sessions):
    console.clear()

    print_routines(routines=routines)

    # get routine type
    while True:
        try:
            routine_index = int(console.input("[bold cyan]Routine index:[/] ")) #INDICES ARE 1-BASED
            routine = manager.get_routine(routine_index) 
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    # print exercises for that routine
    exercise_tree = Tree("Exercises", guide_style="bold cyan")
    for i, exercise in enumerate(routine.exercises, start=1):
        exercise_tree.add(f"[bold]{i}[/bold] · {exercise.name}")
    console.print(exercise_tree)

    # get exercise for report 
    while True:
        try:
            exercise_index = int(console.input("[bold cyan]Choose an exercise:[/] "))
            break
        except ValueError as e:
            console.print(f"[red]{e}[/red]")

    # improve validation 
    if exercise_index < 1 or exercise_index > len(routine.exercises):
        return
    
    try:
        filtered_sessions = filter_sessions_by_routine(sessions=sessions, routine=routine)
    except ValueError:
        exit = input("Return to main menu") or True
        if exit:
            return
    else:
        if not filtered_sessions:
            return

    routine_exercise = routine.exercises[exercise_index - 1]

    report = manager.create_report(routine, filtered_sessions, exercise_index - 1)
    dates = report.get_timeline()
    reps_per_set = report.get_measurements()
    max_reps = report.max_measurement()
    
    # PLOTTING
    x = np.arange(len(dates))  # the label locations
    width = 0.25 
    multiplier = 0
    fig, ax = plt.subplots(layout='constrained')

    for set, reps in reps_per_set.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, reps, width, label=set)
        ax.bar_label(rects, padding=3)
        multiplier += 1
    
    ax.set_ylabel('Rep number')
    ax.set_title(f'Workout report for {routine_exercise.name}')
    ax.set_xticks(x + width, dates)
    ax.legend(loc='upper left', ncols=3)
    ax.set_ylim(0, max_reps)

    plt.show()

    exit = input("Return to main menu") or True
    if exit:
        return

    
