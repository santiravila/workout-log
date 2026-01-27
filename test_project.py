from models import AppManager
from pathlib import Path


def test_routine_creation_service():
    manager = AppManager()

    creation = manager.start_routine_creation("Test Routine")
    creation.add_exercise("Pushups", sets=3, weight=0)
    creation.set_rest(60)
    creation.set_tempo("normal")
    creation.finish()

    routines = manager.get_routines()

    assert len(routines) == 1
    assert routines[0].name == "Test Routine"
    assert len(routines[0].exercises) == 1


def test_session_creation_service():
    manager = AppManager()

    routine_creation = manager.start_routine_creation("Upper Body")
    routine_creation.add_exercise("Bench Press", sets=2, weight=100)
    routine_creation.set_rest(90)
    routine_creation.set_tempo("2-1-2")
    routine_creation.finish()

    routine = manager.get_routines()[0]
    exercise = routine.exercises[0]

    session_creation = manager.start_session_creation(routine)

    session_creation.add_reps(exercise, 8)
    session_creation.add_reps(exercise, 6)
    session_creation.finish()

    sessions = manager.get_sessions()

    assert len(sessions) == 1
    assert sessions[0].exercises[0].reps == [8, 6]


def test_persistence():
    test_storage = Path("data/test_storage.json")
    manager = AppManager(storage_file=test_storage)

    creation = manager.start_routine_creation("Persisted Routine")
    creation.add_exercise("Squats", sets=3, weight=120)
    creation.set_rest(5)
    creation.set_tempo("1-2-3-4")
    creation.finish()

    manager.save_data()

    new_manager = AppManager()
    new_manager.load_data()

    routines = new_manager.get_routines()

    assert len(routines) == 1
    assert routines[0].name == "Persisted Routine"
    assert routines[0].exercises[0].name == "Squats"


def test_report_generator_service():
    manager = AppManager()

    routine_creation = manager.start_routine_creation("Report Routine")
    routine_creation.add_exercise("Bench Press", sets=2, weight=100)
    routine_creation.set_rest(90)
    routine_creation.set_tempo("2-1-2")
    routine_creation.finish()

    routine = manager.get_routines()[0]
    exercise = routine.exercises[0]

    session_creation = manager.start_session_creation(routine)
    session_creation.add_reps(exercise, 8)
    session_creation.add_reps(exercise, 6)
    session_creation.finish()

    session_creation = manager.start_session_creation(routine)
    session_creation.add_reps(exercise, 9)
    session_creation.add_reps(exercise, 7)
    session_creation.finish()

    sessions = manager.get_sessions()

    report = manager.create_report(
        routine=routine,
        sessions=sessions,
        exercise_index=1,
    )

    timeline = report.get_timeline()
    measurements = report.get_measurements()
    max_rep = report.max_measurement()

    assert len(timeline) == 2
    assert measurements[1] == (8, 9)
    assert measurements[2] == (6, 7)
    assert max_rep == 9
