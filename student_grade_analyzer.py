import json
import os
DATA_FILE = "students_data.json"


def load_students():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                return json.load(file)
        except:
            return[]
        
    return[] #this is in case the if is false meaning that the os told us that the file does not exist at all

def save_students(students):
    with open(DATA_FILE,'w') as file:
        json.dump(students, file, indent=4)

students = load_students() # will load the students into the gloable list from teh file

def add_student(): 
    global students
    name = input("Enter your name: ")
    grade = float(input("Enter your grade (0-100): "))

    letter, gpa = get_letter_grade(grade)


    student = {"name": name, "grade": grade, "letter": letter, "gpa":gpa}
    students.append(student)

    save_students(students) #save the one that the user just entered to the file

    print(f"The student {name} is added to the list with the grade {grade} ({letter}) with a gpa of {gpa}")


def display_students (): #students is a list
    if not students:
        print("No student added to the list yet")
        return
    print("\n ------ ALL THE STUDENTS ------")
    for student in students:
        print (f"{student['name']}:{student['grade']} ({student['letter']}) - GPA: {student['gpa']}")
    print()

def calculate_average ():
    if not students:
        print("There is no student in the list")
        return
    total = sum(student['grade'] for student in students)
    average = total/ len(students)
    print(f"\n class average: {average:.2f}")

def find_min_max():
    if not students:
        print ("The list is empty, there is no students")
        return
    
    grades = [student['grade'] for student in students] # improvement: find a way in python where we could keep tarck of who got the highes and lowest grade without needing to search and have a loop
    min_grade = min(grades)
    max_grade = max(grades)

    print(f"The highest grade in the class was: {max_grade}")
    print(f"\nThe lowest grade in the class was: {min_grade}")


def calculate_median():
    if not students:
        print("There is no student in the list")
        return
    
    grades = sorted(student['grade'] for student in students)
    n = len(grades)

    if (n % 2 == 0):
        median = (grades[n//2] + grades[n//2 - 1])/2
    else:
        median = grades[n//2]

    print(f"\n Median Grade: {median:.2f}")

def sort_students():
    if not students:
        print("no students is in the list")
        return
    sorted_students = sorted(students, key= lambda x: x['grade'], reverse=True)
    print("\n ------------ STUDENTS (SORTED BY GRADES) -------------")
    for i, student in enumerate (sorted_students, 1):   #here is much more like c we keep track of teh iterationthe i, I have the value of the i, and the 1 tells it to start from 1 sonce teh default is 0
        print(f"{i}. {student['name']}: {student['grade']}")
    print()

def get_letter_grade(grade):
        
    if grade >=97:
        gpa = 4.0
        letter = 'A+'
    elif grade >=93:
        gpa = 4.0
        letter = 'A'
    elif grade >=90:
        gpa = 3.7
        letter = 'A-'
    elif grade >= 87:
        gpa = 3.3
        letter = 'B+'
    elif grade >= 83:
        gpa = 3.0
        letter = 'B'
    elif grade >= 80:
        gpa = 2.7
        letter = 'B-'
    elif grade >= 77:
        gpa = 2.3
        letter = 'C+'
    elif grade >= 73:
        gpa = 2.0
        letter = 'C'
    elif grade >= 70:
        gpa = 1.7
        letter = 'C-'
    elif grade >= 67:
        gpa = 1.3
        letter = 'D+'
    elif grade >= 60:
        gpa = 1.0
        letter = 'D'
    else: 
        gpa = 0.0
        letter = 'F'

    return letter, gpa

def calculate_class_avGPA():
    total_gpa = 0
    for student in students:
        gpa = student['gpa']
        total_gpa += gpa

    avg_gpa = total_gpa / len(students)

    print(f"\n CLASS AVERAGE GPA: {avg_gpa:.2f}")
    print()
        

def grade_distribution():
    if not students:
        print("No students in the system")
        return
    
    a_count = 0
    b_count = 0
    c_count = 0
    failing_count = 0   #how many students failed concidering that failing is below 70%z

    for student in students:
        letter = student['letter']

        if letter == 'A+' or letter == "A" or letter == "A-":
            a_count +=1
        elif letter == 'B+' or letter == "B" or letter == "B-":
            b_count +=1       
        elif letter == 'C+' or letter == "C" or letter == "C-":
            c_count +=1   
        else:
            failing_count += 1

    
    print(f"THERE ARE {len(students)}")
    print(f"Number of students who got (A+, A, A-): {a_count}")
    print(f"Number of students who got (B+, B, B-): {b_count}")
    print(f"Number of students who got (C+, C, C-): {c_count}")
    print(f"Number of students who FAILED {failing_count}")
    print()


def search_student():
    if not students:
        print("There is no student in the system")
        return
    
    search_name = input("Enter the name of the student to search for: ").lower()


    found = False
    for student in students:
        if search_name in student['name'].lower():
            print (f"\n Found: {student['name']} - Grade: {student['grade']} ({student['letter']}) - GPA: {student['gpa']}")
            found = True

    if not found:
        print(f"\nNo student foound with name '{search_name}'")
            


def main():

    if students:
        print(f" {len(students)} student(s) are loaded from the file\n")

    
    while True:
        print(" ------ STUDENT GRADE ANALYZER ------")
        print("1. ADD STUDENTS")
        print("2. DISPLAY STUDENTS")
        print("3. CALCULATE AVERAGE")
        print("4. FIND MIN/MAX GRADES")
        print("5. CALCULATE MEDIAN")
        print("6. SORT STUDENTS BY GRADE")
        print("7. CALCULATE CLASS AVEREAGE GPA")
        print("8. SEE CLASS DISTRIBUTION")
        print("9. SEARCH STUDENT")
        print("10.EXIT")       

        while True:  #this is like a do while loop, since it does not exist in python
            choice = input ("Enter choice: ") #no need to conver to an int since i only need the value i wont be doing any arithmatic operations on them
            if choice in ["1", "2", "3","4","5","6","7","8","9","10"]:
                break
            else:
                print("Invalid input, please enter a valid number")


        if choice == "1":
            add_student()
        elif choice == "2":
            display_students()
        elif choice == "3":
            calculate_average() 
        elif choice =="4":
            find_min_max()
        elif choice =="5":
            calculate_median()
        elif choice == "6":
            sort_students() 
        elif choice =="7":
            calculate_class_avGPA()
        elif choice =="8":
            grade_distribution()
        elif choice == "9":
            search_student()  
        else:
            print("GOODBYE!!")
            break

if __name__ == "__main__":   # this controlls when the main runs, it tell it to run only if it is the main funtion and not if it is impoted, since if it is imported it will have another name (the name of the function)
    main()



        

