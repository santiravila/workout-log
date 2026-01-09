from models import AppManager
import pytest
from datetime import date

def test_create_routine_increases_count():
    manager = AppManager()
    initial_count = len(manager.routines)    

    manager.create_routine(
        "name", 
        5.4, 
        "1-2-3-4", 
        [{"name": "pushups", "sets": 1, "weight": 5}]
    )
    
    assert len(manager.routines) == initial_count + 1   


def test_create_routine_creates_valid_routine():
    manager = AppManager()

    routine = manager.create_routine(
        "name", 
        5.4, 
        "1-2-3-4",
        [{"name": "pushups", "sets": 1, "weight": 5}]
    )

    assert routine.name == "name"
    assert routine.rest == 5.4
    assert routine.exercises[0].name == "pushups"


def test_get_routine_finds():
    manager = AppManager()
    routine = manager.create_routine(
        "name", 
        5.4, 
        "1-2-3-4",
        [{"name": "pushups", "sets": 1, "weight": 5}]
    )
    
    assert manager.get_routine("name") == routine
    assert manager.get_routine("something wrong") is None


def test_create_session_increases_count():
    manager = AppManager()
    initial_count = len(manager.sessions)    

    routine = manager.create_routine(
        "name", 
        5.4, 
        "1-2-3-4",
        [{"name": "pushups", "sets": 1, "weight": 5}]
    )

    manager.create_session(
        "name", 
        [{"name": "pushups", "sets": 1, "weight": 5}]
    )
    
    assert len(manager.sessions) == initial_count + 1  


def test_persistence(tmp_path):
    d = tmp_path / "junk"
    d.mkdir()
    p = d / "test_storage.json"
    
    manager = AppManager()
    manager.file_path = str(p)
    
    manager.create_routine("TestRoutine", 1.0, "1-2-3-4", [])
    
    manager.save_data()
    
    assert p.exists()
    
    new_manager = AppManager()
    new_manager.file_path = str(p)
    new_manager.load_data()
    
    assert len(new_manager.routines) == 1
    assert new_manager.routines[0].name == "TestRoutine"