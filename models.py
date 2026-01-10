from datetime import date
from copy import deepcopy
import json


class Exercise:
    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def __init__(
        self, name: str, sets: int, weight: float, reps: list[int] | None = None
    ):
        self.name = name
        self.sets = sets
        self.weight = weight
        self.reps = [] if reps is None else reps

    def __eq__(self, other):
        if not isinstance(other, Exercise):
            return NotImplemented
        return (
            self.name == other.name
            and self.sets == other.sets
            and self.weight == other.weight
            and self.reps == other.reps
        )

    def __str__(self):
        return f"Exercise name: {self.name} | Sets: {self.sets} | Weight: {self.weight} | Reps: {self.reps}"

    def to_dict(self):
        return {
            "name": self.name,
            "sets": self.sets,
            "weight": self.weight,
            "reps": self.reps,
        }


class Session:
    @classmethod
    def from_dict(cls, data: dict):
        if "date" in data:
            data["date"] = date.fromisoformat(data["date"])
        
        data["exercises"] = [Exercise.from_dict(exercise) for exercise in data["exercises"]]

        return cls(**data)

    def __init__(
        self, id: int, routine_name: str, date: date, exercises: list[Exercise]
    ) -> None:
        self.id = id
        self.date = date
        self.exercises = exercises
        self.routine_name = routine_name

    def __str__(self):
        return f"Routine name: {self.routine_name}, Workout Date: {self.date}"

    def to_dict(self):
        return {
            "id": self.id,
            "routine_name": self.routine_name,
            "date": self.date.isoformat(),
            "exercises": [exercise.to_dict() for exercise in self.exercises],
        }


class Routine:
    @classmethod
    def from_dict(cls, data: dict):
        data["exercises"] = [Exercise.from_dict(exercise) for exercise in data["exercises"]]
        return cls(**data)

    def __init__(
        self, id: int, name: str, rest: float, tempo: str, exercises: list[Exercise]
    ):
        self.id = id
        self.name = name
        self.rest = rest
        self.tempo = tempo
        self.exercises = exercises

    def __eq__(self, other):
        if not isinstance(other, Routine):
            return NotImplemented
        return (
            self.name == other.name
            and self.rest == other.rest
            and self.tempo == other.tempo
            and self.exercises == other.exercises
        )

    def __str__(self):
        return f"Routine name: {self.name} | Rest: {self.rest} | Tempo: {self.tempo}"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rest": self.rest,
            "tempo": self.tempo,
            "exercises": [exercise.to_dict() for exercise in self.exercises],
        }


class RoutineCreation:
    def __init__(self, manager, name: str):
        if name in [routine.name for routine in manager.routines]:
            raise ValueError("Routine already exists")

        self.manager = manager
        self.name = name

        self.exercises = []
        self.rest = None
        self.tempo = None

    def add_exercise(self, name: str, sets: int, weight: float):
        if sets <= 0:
            raise ValueError("Sets must be positive")
        
        if weight < 0:
            raise ValueError("Weight cannot be negative")
        exercise = Exercise(name, sets, weight)
        self.exercises.append(exercise)

    def set_rest(self, rest: float):
        if rest < 0:
            raise ValueError("Rest cannot be negative")
        self.rest = rest
    
    def set_tempo(self, tempo: str):
        if not tempo:
            raise ValueError("Tempo cannot be empty")
        self.tempo = tempo

    def finish(self) -> Routine | None:
        if not self.exercises:
            raise ValueError("Routine must have at least one exercise")
        
        if self.rest is None or self.tempo is None:
            raise ValueError("Routine is incomplete")
        
        routine_id = len(self.manager.routines) + 1

        routine = Routine(
            routine_id,
            self.name,
            self.rest,
            self.tempo,
            self.exercises
        )

        self.manager.routines.append(routine)
        return routine


class AppManager:
    def __init__(self) -> None:
        self.routines = [] 
        self.sessions = [] 
        self.file_path = "data/storage.json"

    def start_routine_creation(self, name: str) -> RoutineCreation:
        return RoutineCreation(self, name)

    def get_routine(self, name: str) -> Routine | None:
        for routine in self.routines:
            if routine.name == name:
                return deepcopy(routine)
        return None

    def create_session(self, routine_name: str, exercises_data: list[dict]):
        # Deserialization
        exercises_with_reps = [Exercise(**exercise) for exercise in exercises_data]
        session_id = len(self.sessions) + 1
        new_session = Session(
            session_id, routine_name, date.today(), exercises_with_reps
        )
        self.sessions.append(new_session)
        return new_session

    def save_data(self):
        data = {
            "routines": [r.to_dict() for r in self.routines],
            "sessions": [s.to_dict() for s in self.sessions],
        }

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)

            for routine in data["routines"]:
                loaded_routine = Routine.from_dict(routine)
                if loaded_routine is not None:
                    self.routines.append(loaded_routine)

            for session in data["sessions"]:
                loaded_session = Session.from_dict(session)
                if loaded_session is not None:
                    self.sessions.append(loaded_session)
        except FileNotFoundError:
            pass