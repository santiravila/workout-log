from models import AppManager


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

    # Create routine
    routine_creation = manager.start_routine_creation("Upper Body")
    routine_creation.add_exercise("Bench Press", sets=2, weight=100)
    routine_creation.finish()

    routine = manager.get_routines()[0]

    # Create session
    session_creation = manager.start_session_creation(routine)
    session_creation.add_reps("Bench Press", [8, 6])
    session_creation.finish()

    sessions = manager.get_sessions()

    assert len(sessions) == 1
    assert sessions[0].exercises[0].reps == [8, 6]


def test_persistence_roundtrip(tmp_path, monkeypatch):
    manager = AppManager()

    # Create routine
    creation = manager.start_routine_creation("Persisted Routine")
    creation.add_exercise("Squats", sets=3, weight=120)
    creation.finish()

    # Patch storage file location
    from models import STORAGE_FILE
    monkeypatch.setattr("models.STORAGE_FILE", tmp_path / "data.json")

    manager.save_data()

    # Reload
    new_manager = AppManager()
    monkeypatch.setattr("models.STORAGE_FILE", tmp_path / "data.json")
    new_manager.load_data()

    routines = new_manager.get_routines()

    assert len(routines) == 1
    assert routines[0].name == "Persisted Routine"
    assert routines[0].exercises[0].name == "Squats"


def test_report_generator_service():
    manager = AppManager()

    # Create routine
    routine_creation = manager.start_routine_creation("Report Routine")
    routine_creation.add_exercise("Bench Press", sets=2, weight=100)
    routine_creation.finish()

    routine = manager.get_routines()[0]

    # Create sessions
    session_creation = manager.start_session_creation(routine)
    session_creation.add_reps("Bench Press", [8, 6])
    session_creation.finish()

    session_creation = manager.start_session_creation(routine)
    session_creation.add_reps("Bench Press", [9, 7])
    session_creation.finish()

    sessions = manager.get_sessions()

    # Generate report
    report = manager.create_report(
        routine=routine,
        sessions=sessions,
        exercise_index=1,
    )

    timeline = report.get_timeline()
    measurements = report.get_measurements()
    max_rep = report.max_measurement()

    assert len(timeline) == 2
    assert len(measurements) == 2
    assert max_rep == 9
