# Workout Log

## Video Demo: URL Here

## Description:
I had been tracking my workouts in iOS Notes and realized I was doing too much copy-pasteing among other inefficient practices, specially managing several exercise routines within the week. I found value in the idea of representing exercise routines as blueprints for creating workout sessions in order to save time every time I log a session. And thats basically the base premise of this program. 

Initially, the program allows the user to:

- Create routines 
- Create workout sessions from one of the existing routines (if any)

 This already saves time when creating sessions. However, the greatest added value comes when there are already workout sessions logged, because you can:
 - Filter logged sessions by their routine type
 - Generate plot-based performance reports that show the timeline of reps per set of a certain exercise throughout all workout sessions of a routine type. 

These two features, respectively, make it easier to skim through logged sessions in a more organized way, and graphically visualize performance over time, enhancing decision-making and user friendliness.

## Files Overview

### project.py
This file is the orchestrator of the program. It's job is to determine the program's flow based on user input and to provide the interfaces the state they need, in this case, the saved routines and workout sessions. It also is in charge of loading data from storage files into the program and of saving data after all changes to the program state are done.

### controller.py
I made this file to avoid circular dependencies and centralize access to the program's manager.

### models.py
This file contains the data models and services that actually store the logic of the program. 

### views.py
This is where interaction with the user happens. Displaying menus, styling, getting input, basic validation, visualization and delegation to models.py for program state and logic.

### test_project.py
Unit tests for each of the services in models.py and for checking persistance.

---

## Program Flow
1. Select an option in the main menu
2. Follow the instructions for each option
3. Return to main menu
4. Exit
---

## Data Model

### Exercise
It bundles data related to a given exercise. Generally used as an aggregate for Routine and Session classes.
Its signature is (self, name: str, sets: int, weight: float, reps: list[int] | None = None)

### Routine
Its the blueprint for session creation.
Its signature is: (self, id: int, name: str, rest: float, tempo: str, exercises: list[Exercise])

### Session
This data model contains all data related to a specific workout session, the actual, logged data. Differs to Routine in the sense that it has a date of creation and a routine name that it inherits from so to speak.
Its signature is: (self, id: int, routine_name: str, date: datetime, exercises: list[Exercise])

---

## Design Choices

### Architecture and Separation of Concerns
Initially I took a procedural approach implementing it all in the main file. However, as the project grew larger and more complex, it began to be hard even for myself to come back to it every day and understand what I had. I started researching about design patterns and MVC caught my attention because of its clarity and compatibility with my project, and so I began refactoring my code to create separation of concerns by decoupling user interface, program state and logic as well as the data models and services. Migrating from procedural thinking to a modular, single-responsible and decoupled one was hard and took me some time to implement the refactorings necessary, but the time I spent thinking and implementing at the design and architectural level greatly paid off as overall time saved, and a project I can come back to, understand, and continue evolving over time, which I plan to do.

Although CS50P requires testing of top-level functions in project.py, as I said, I chose to concentrate the program’s core logic in dedicated service classes to keep responsibilities well separated and the codebase easier to extend

---

## Persistence
The program uses JSON-based persistance, which is implemented in the program manager at models.py. 
- Loading: Reads the contents of the JSON and populates the state data structures (routines, sessions) with the result of converting the data from dictionaries to the actual classes (through from_dict() class methods)
- Saving: converting the routines and classes in the program state into dictionaries and writing them to the storage file.

---


## How to Run
start virtual environment (bash): 

    source .venv/Scripts/activate 
run     

    python project.py
---
