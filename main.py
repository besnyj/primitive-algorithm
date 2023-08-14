import sqlite3
import threading
import queue

# global variables
patient_queue = queue.Queue()
chance_list = []


def is_working(function): # dedcoration for debug functions
        def wrapper(*args, **kwargs):
            try:
                function(*args, **kwargs)
                fname = function.__name__
                print(f"{fname} WORKED SUCCESSFULLY")
            except:
                print("ERROR")
        return wrapper


## table name patients, values: name TEXT, age INTEGER, gender TEXT, weight INTEGER.
connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def add_patient(name, age, gender, weight):

    cursor.execute("""
    INSERT INTO patients VALUES
    ('{}', '{}', '{}', '{}')
                   """.format(name, age, gender, weight))
    connection.commit()


def patient_queue_generator():
    global patient_queue
    
    cursor.execute("""
    SELECT * FROM patients
                """)
    patient_list = cursor.fetchall()

    for patient in patient_list:
        patient_queue.put(patient)


# I HAVE NO IDEA WHAT IS THE HEART ATTACK FORMULA, SO I'M MAKING ONE UP JUST FOR THE SAKE OF SIMPLICITY
def calculate_chance():
        global chance_list
        
        while True:
            patient = patient_queue.get()
            age = patient[1]
            weight = patient[3]
            if patient[2] == "Male":
                y = 0.5
            elif patient[2] == "Female":
                y = 0.3  
            chanceOfHeartAttack = (weight/age)*y
            chance_list.append(chanceOfHeartAttack)
            if patient_queue.empty():
                break


patient_queue_generator()


def start_threadings():
    
    t1 = threading.Thread(target=calculate_chance)          
    t2 = threading.Thread(target=calculate_chance)
    t3 = threading.Thread(target=calculate_chance)

    t1.start()
    t2.start()
    t3.start()
    
    print("Im working")


start_threadings()




