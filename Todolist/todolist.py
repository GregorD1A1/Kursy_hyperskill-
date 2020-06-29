# importy
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

# defenicje klas, funkcji i inne preludia
engine = create_engine("sqlite:///todo.db?check_same_thread=False")
Baza_czyli_klasa_rodziczna_databazy = declarative_base()

class Tabela(Baza_czyli_klasa_rodziczna_databazy):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Baza_czyli_klasa_rodziczna_databazy.metadata.create_all(engine)

Sesion = sessionmaker(bind=engine, autocommit=True)
sesja = Sesion()

def print_menu():
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")

def show_todays_tasks():
    print(datetime.today().strftime("Today %d %b"))
    zadania = sesja.query(Tabela).filter(Tabela.deadline == datetime.today().date()).all()
    if len(zadania) == 0:
        print("Nothing to do!")
    else:
        for nr, zadanie in enumerate(zadania): print("{0}) {1}".format(nr + 1, zadanie))
    print("")

def show_weeks_tasks():
    for days_delta in range(7):
        dzien = datetime.today() + timedelta(days=days_delta)
        print(dzien.strftime("%A %d %b"))
        zadania = sesja.query(Tabela).filter(Tabela.deadline == dzien.date()).all()
        if len(zadania) == 0:
            print("Nothing to do!")
        else:
            for nr, zadanie in enumerate(zadania): print("{0}) {1}".format(nr + 1, zadanie))
        print("")

def show_all_tasks():
    print("All tasks:")
    zadania = sesja.query(Tabela).all()
    if len(zadania) == 0:
        print("Nothing to do!")
    else:
        for nr, zadanie in enumerate(zadania): print(zadanie.deadline.strftime("{0}) {1}. %d %b".format(nr + 1, zadanie)))
    print("")

def show_missed_tasks():
    print("Missed tasks:")
    zadania = sesja.query(Tabela).filter(Tabela.deadline < datetime.today().date()).all()
    if len(zadania) == 0:
        print("Nothing is missed!")
    else:
        for nr, zadanie in enumerate(zadania): print(zadanie.deadline.strftime("{0}) {1}. %d %b".format(nr + 1, zadanie)))
    print("")

def delete_task():
    print("Chose the number of the task you want to delete:")
    zadania = sesja.query(Tabela).all()
    if len(zadania) == 0:
        print("Nothing to delete!")
    else:
        for nr, zadanie in enumerate(zadania): print(zadanie.deadline.strftime("{0}) {1}. %d %b".format(nr + 1, zadanie)))
    sesja.delete(zadania[int(input()) - 1])

def add_task():
    print("Enter task")
    taskk = input()
    print("Enter deadline")
    deadlinee = input()
    nowy_wiersz = Tabela(task=taskk, deadline=datetime.strptime(deadlinee, '%Y-%m-%d').date())
    print(nowy_wiersz)
    sesja.add(nowy_wiersz)
    print("Task has been added!")

# program główny
while True:
    print_menu()
    akcja_nr = int(input())
    if akcja_nr == 1:
        show_todays_tasks()
    elif akcja_nr == 2:
        show_weeks_tasks()
    elif akcja_nr == 3:
        show_all_tasks()
    elif akcja_nr == 4:
        show_missed_tasks()
    elif akcja_nr == 5:
        add_task()
    elif akcja_nr == 6:
        delete_task()
    elif akcja_nr == 0:
        print("Bye!")
        break
