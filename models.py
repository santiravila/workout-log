from datetime import date
from copy import deepcopy


class Exercise:
    def __init__(self, name: str, sets: int, weight: float, reps: list[int] | None = None):
        self.name = name
        self.sets = sets
        self.weight = weight
        self.reps = [] if reps is None else reps

    def __eq__(self, other):
        if not isinstance(other, Exercise):
            return NotImplemented
        return (
            self.name == other.name and
            self.sets == other.sets and
            self.weight == other.weight and
            self.reps == other.reps
        )

    def __str__(self):
        return f"Exercise name: {self.name} | Sets: {self.sets} | Weight: {self.weight} | Reps: {self.reps}"


class Session:
    def __init__(self, id: int, routine_name: str, date: date, exercises: list[Exercise]) -> None:
        self.id = id
        self.date = date
        self.exercises = exercises
        self.routine_name = routine_name

    def __str__(self):
        return f"Routine name: {self.routine_name}, Workout Date: {self.date}"


class Routine:
    def __init__(self, id: int, name: str, rest: float, tempo: str, exercises: list[Exercise]):
        self.id = id
        self.name = name
        self.rest = rest
        self.tempo = tempo
        self.exercises = exercises

    def __eq__(self, other):
        if not isinstance(other, Routine):
            return NotImplemented
        return (
            self.name == other.name and
            self.rest == other.rest and
            self.tempo == other.tempo and
            self.exercises == other.exercises
        )
    
    def __str__(self):
        return f"Routine name: {self.name} | Rest: {self.rest} | Tempo: {self.tempo}"


class AppManager:
    def __init__(self, routines: list[Routine] | None = None, sessions: list[Session] | None = None) -> None:
        self.routines = [] if routines is None else routines
        self.sessions = [] if sessions is None else sessions

    def create_routine(self, routine_name: str, rest: float, tempo: str, exercise_data: list[dict]):
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
        new_session = Session(session_id, routine_name, date.today(), exercises_with_reps)
        self.sessions.append(new_session)
        return new_session        

            