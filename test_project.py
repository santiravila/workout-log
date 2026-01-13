import pytest
from models import AppManager


def test_create_routine_increases_count():
    manager = AppManager()
    initial_count = len(manager.routines)

    creation = manager.start_routine_creation("name")
    creation.add_exercise("pushups", 1, 5)
    creation.set_rest(5.4)
    creation.set_tempo("1-2-3-4")
    creation.finish()

    assert len(manager.routines) == initial_count + 1


def test_create_routine_creates_valid_routine():
    manager = AppManager()

    creation = manager.start_routine_creation("name")
    creation.add_exercise("pushups", 1, 5)
    creation.set_rest(5.4)
    creation.set_tempo("1-2-3-4")
    routine = creation.finish()

    if routine:
        assert routine.name == "name"
        assert routine.rest == 5.4
        assert routine.exercises[0].name == "pushups"


def test_get_routine_finds():
    manager = AppManager()

    creation = manager.start_routine_creation("name")
    creation.add_exercise("pushups", 1, 5)
    creation.set_rest(5.4)
    creation.set_tempo("1-2-3-4")
    routine = creation.finish()

    assert manager.get_routine("name") == routine

    with pytest.raises(ValueError):
        manager.get_routine("something wrong")


def test_create_session_increases_count():
    manager = AppManager()
    initial_count = len(manager.sessions)

    routine_creation = manager.start_routine_creation("name")
    routine_creation.add_exercise("pushups", 1, 5)
    routine_creation.set_rest(5.4)
    routine_creation.set_tempo("1-2-3-4")
    routine_creation.finish()

    routine = manager.get_routine("name")
    session_creation = manager.start_session_creation(routine)
    session_creation.add_reps(routine.exercises[0], 0, 10)
    session_creation.finish()

    assert len(manager.sessions) == initial_count + 1


def test_persistence(tmp_path):
    p = tmp_path / "test_storage.json"

    manager = AppManager()
    manager.file_path = str(p)

    creation = manager.start_routine_creation("TestRoutine")
    creation.add_exercise("pushups", 1, 5)
    creation.set_rest(1.0)
    creation.set_tempo("1-2-3-4")
    creation.finish()

    manager.save_data()
    assert p.exists()

    new_manager = AppManager()
    new_manager.file_path = str(p)
    new_manager.load_data()

    assert len(new_manager.routines) == 1
    assert new_manager.routines[0].name == "TestRoutine"
