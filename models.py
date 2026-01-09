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


class AppManager:
    def __init__(
        self,
        routines: list[Routine] | None = None,
        sessions: list[Session] | None = None,
    ) -> None:
        self.routines = [] if routines is None else routines
        self.sessions = [] if sessions is None else sessions
        self.file_path = "data/storage.json"

    def create_routine(
        self, routine_name: str, rest: float, tempo: str, exercise_data: list[dict]
    ):
        # Deserialization
        exercise_list = [Exercise(**exercise) for exercise in exercise_data]
        routine_id = len(self.routines) + 1
        new_routine = Routine(routine_id, routine_name, rest, tempo, exercise_list)
        self.routines.append(new_routine)
        return new_routine

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