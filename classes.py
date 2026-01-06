from datetime import date

class Exercise:
    def __init__(self, name: str, sets: int, weight: float, reps: list[int] = []):
        self.name = name
        self.sets = sets
        self.weight = weight
        self.reps = reps

    def __str__(self):
        return f"Exercise name: {self.name} | Sets: {self.sets} | Weight: {self.weight} | Reps: {self.reps}"


class Session:
    def __init__(self, id: int, routine_name: str, date: date, exercises: list[Exercise]) -> None:
        self.id = id
        self.date = date
        self.exercises = exercises
        self.routine_name = routine_name

    def assign_reps_to_sets(self, reps):
        for exercise in self.exercises:
            exercise.reps = reps

    def __str__(self):
        return f"Routine name: {self.routine_name}, Workout Date: {self.date}"


class Routine:
    def __init__(self, id: int, name: str, rest: float, tempo: str, exercises: list[Exercise]):
        self.id = id
        self.name = name
        self.rest = rest
        self.tempo = tempo
        self.exercises = exercises

    def get_exercises(self):
        return self.exercises

    def __str__(self):
        return f"Routine name: {self.name} | Rest: {self.rest} | Tempo: {self.tempo}"


class AppManager:
    ...







