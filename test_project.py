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