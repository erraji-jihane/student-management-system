import json
import os
DATA_FILE = "students_data.json"
DATA_VERSION = 2
students = []



def load_students():
    """Load students from JSON file"""
    global students
    
    if not os.path.exists(DATA_FILE):
        students = []
        print("No existing data file. Starting fresh.")
        return
    
    try:
        with open(DATA_FILE, 'r') as file:
            students = json.load(file)
            print(f"Loaded {len(students)} student(s) from file.")
                
    except json.JSONDecodeError:
        students = []
        print("Corrupted file. Starting fresh.")
    except Exception as e:
        students = []
        print(f"Error loading file: {e}. Starting fresh.")


def save_students(students):
    """Save students directly as list"""
    with open(DATA_FILE, 'w') as file:
        json.dump(students, file, indent=4)


load_students()

def get_letter_and_gpa(grade):
        
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

def calculate_weighted_gpa(student):
    if not student ['courses']:
        student ['weighted_gpa'] = 0.0
        student['total_credits'] = 0
        return
    
    total_grade_points = 0
    total_credits = 0

    for course in student['courses']:
        grade = course ['grade']
        letter, gpa = get_letter_and_gpa(grade)
        grade_points = gpa * course['credits']
        total_grade_points += grade_points
        total_credits +=course['credits']
    
    student['weighted_gpa'] = round(total_grade_points / total_credits, 2)
    student['total_credits'] = total_credits 

def search_course(search_course):  
    students_enrolled_in_course =[]

    if not students:
        print("There is no student in the system")
        return

    for student in students:
        for course in student.get('courses', []):
            if search_course in course['course_name'].lower():
                students_enrolled_in_course.append({
                    'student_ID': student['student_id'],
                    'student_name': student['name'],
                    'grade':course['grade'],
                    'letter': course['letter'],
                    'credits': course['credits']
                })

                
    return students_enrolled_in_course  


#---------------------------------------------------------MENU METHODS ------------------------------------------------------------------

def add_student(): 
    global students
    name = input("Enter student name: ")
    stud_id = len(students) +1

    student = {
        "student_id": stud_id,
        "name": name,
        "courses": [],  
        "total_credits":0,
        "weighted_gpa": 0.0

    }
    students.append(student)
    save_students(students) 

    print(f"The student {name} - {stud_id} is added to the list. Use add course to add course name if needed")

def delete_student():
    global students
    if not students:
        print("\n No students to delete!")
        return
    
    for student in students:
        print(f"ID {student['student_id']}: {student['name']}")

    try:
        deleted_id = int(input("\nEnter student iD to delete: "))

        student_to_delete = None
        for student in students:
            if student ['student_id']== deleted_id:
                student_to_delete = student
                break
        if not student_to_delete:
            print(f"\n Student ID {deleted_id} not found!")
            return
        confirm = input(f"Delete {student_to_delete['name']}? (yes/no): ").lower()
        if confirm == 'yes':
            students.remove(student_to_delete)
            save_students(students)
            print(f"\n {student_to_delete['name']} deleted!")
        else:
            print("\n Cancelled.")
    except ValueError:
        print("\n Invalid ID")
    
def search_student(search_id):
    if not students:
        print("There is no student in the system")
        return []
    
    for student in students:
        if student.get('student_id') == search_id:  
            return student
    
    return None

def display_students (): 
    if not students:
        print("No student added to the list yet")
        return
    print("\n ------ ALL THE STUDENTS ------")
    for student in students:
        print (f"{student['name']}:{student['student_id']} ({student['total_credits']}) credits - GPA: {student['weighted_gpa']}")
    print()

def calculate_average_GPA ():
    if not students:
        print("There is no student in the list")
        return
    total = sum(student.get('weighted_gpa', 0.0) for student in students)
    average = total/ len(students)
    print(f"\n class average GPA: {average:.2f}")

def sort_students_by_GPA():
    if not students:
        print("no students is in the list")
        return
    sorted_students = sorted(students, key= lambda x: x['weighted_gpa'], reverse=True)
    print("\n ------------ STUDENTS (SORTED BY GRADES) -------------")
    for i, student in enumerate (sorted_students, 1):   
        print(f"{i}. {student['name']}: {student['student_id']  } -> {student['weighted_gpa']}")
    print()

#-----------------------------------------------------COURSE RELATED METHODS ----------------------------------------------------------

def add_course_to_student():
    search_id = int(input("please enter the student's id"))

    searched_student= search_student(search_id)
    
    if not searched_student:
        print("\n student not found!")
        return
    print (f"\n------Adding course for {searched_student['name']} (ID: {search_id})------")

    course_name =input("course name: ")
    grade = float(input("Grade (0-100: "))
    credits = int(input("Credit hours: "))

    if not (0<= grade <= 100):
        print("\n Grade must be between 0-100!")
        return
    if credits <= 0:
        print ("\n Credits must be positive!")
        return
    
    letter, gpa = get_letter_and_gpa(grade)

    course = {
        "course_name": course_name,
        "grade": grade,
        "letter": letter,
        "credits": credits
    }
    searched_student['courses'].append(course)

    calculate_weighted_gpa(searched_student)

    save_students(students)

    print(f"\n '{course_name}' added to {searched_student['name']}!")
    print(f"   Grade: {grade} ({letter}), Credits: {credits}")
    print(f"   New GPA: {searched_student['weighted_gpa']:.2f}")

def find_min_max():
    if not students:
        print ("The list is empty, there is no students")
        return
    
    target_course = input("please enter the course code: ")
    grades = []

    students_enrolled_in_course = search_course(target_course)

    if not students_enrolled_in_course:
        print("no students enrolled in this course")
        return
    for student in students_enrolled_in_course:
        grades.append(student['grade'])

                                  
    min_grade = min(grades)
    max_grade = max(grades)

    print(f"The highest grade in the class was: {max_grade}")
    print(f"\nThe lowest grade in the class was: {min_grade}")

def calculate_median():
    if not students:
        print("There is no student in the list")
        return
    
    target_course = input("please enter the course code: ")
    students_enrolled_in_course = search_course(target_course)

    if not students_enrolled_in_course:
        print("No student enrolled in this course")
        return
    grades=[]
    for student in students_enrolled_in_course:
        grades.append(student['grade'])
    
    grades = sorted (grades)

    n = len(grades)

    if (n % 2 == 0):
        median = (grades[n//2] + grades[n//2 - 1])/2
    else:
        median = grades[n//2]

    print(f"\n Median Grade: {median:.2f}")


def sort_students_by_grade(): 
    if not students:
        print("no student in the system")
        return
    
    target_course = input("Please enter the course code: ")
    enrolled_students = search_course(target_course)
    
    if not enrolled_students:
        print(f"No student enrolled in {target_course} ")
        return
    
    sorted_students = sorted(enrolled_students, key= lambda x: x['grade'], reverse=True)
    print(f"\n ------------ STUDENTS ENROLLED IN {target_course}(SORTED BY GRADES) -------------")
    for i, student in enumerate (sorted_students, 1):
        print(f"{i}. {student['student_name']}: {student['student_ID']  } -> {student['grade']} ({student ['letter']})")
    print ()


def class_average_grade():  
    
    if not students:
        print("No students in system")
        return

    target_course = input("Enter the course code: ")
    students_enrolled_in_course = search_course(target_course)

    if not students_enrolled_in_course:
        print(f"no student enrolled in {target_course}")
        return

    total_grade = sum(s['grade'] for s in students_enrolled_in_course)

    avg_gpa = total_grade / len(students_enrolled_in_course)

    print(f"\n CLASS AVERAGE GPA: {avg_gpa:.2f}")
    print()
        
def grade_distribution():
    if not students:
        print("No students in the system")
        return
    target_course = input("Please enter the course code:")
    student_enrolled_in_course = search_course(target_course)

    if not student_enrolled_in_course:
        print("No student is enrolled in this course")
        return
    
    a_count = 0
    b_count = 0
    c_count = 0
    failing_count = 0   

    for student in student_enrolled_in_course:
        letter = student['letter']

        if letter == 'A+' or letter == "A" or letter == "A-":
            a_count +=1
        elif letter == 'B+' or letter == "B" or letter == "B-":
            b_count +=1       
        elif letter == 'C+' or letter == "C" or letter == "C-":
            c_count +=1   
        else:
            failing_count += 1

    
    print(f"THERE ARE {len(student_enrolled_in_course)}")
    print(f"Number of students who got (A+, A, A-): {a_count}")
    print(f"Number of students who got (B+, B, B-): {b_count}")
    print(f"Number of students who got (C+, C, C-): {c_count}")
    print(f"Number of students who FAILED {failing_count}")
    print()





#-------------------------------------------------------------- MAIN -------------------------------------------------------------------------------

def main():

    if students:
        print(f" {len(students)} student(s) are loaded from the file\n")

    
    while True:
        print(" --------------------------------- STUDENTS GRADES ALYZER --------------------------------- ")
        print("1. ADD STUDENTS")
        print("2. DELETE STUDENT") 
        print("3. SEARCH STUDENT")
        print("4. DISPLAY ALL STUDENTS")
        print("5. CALCULATE AVERAGE GPA OF ALL STUDENTS")
        print("6. SORT STUDENTS BY GPA")
        print("\n ---------- COURSE RELATED CHOICES ----------")
        print("7. ADD COURSE TO STUDENT")
        print("8. FIND MIN/MAX GRADES IN A COURSE")
        print("9. CALCULATE THE MEDIAN OF THS CLASS")
        print("10.  SEE STUDENTS ENROLLED IN A COURSE SORTED BY GRADE")
        print("11. CALCULATE CLASS AVERAGE GRADE")
        print("12. SEE CLASS GRADES DISTRIBUTION")
        
        print("13.EXIT")       

        while True:  
            choice = input ("Enter choice: ") 
            if choice in ["1", "2", "3","4","5","6","7","8","9","10","11", "12", "13"]:
                break
            else:
                print("Invalid input, please enter a valid number")


        if choice == "1":
            add_student()
        elif choice == "2":
            delete_student()  
        elif choice == "3":
            try:
                target_student = int(input("Enter student Id:"))
                student = search_student(target_student) 

                if student:
                    print(f"\n Found: {student['name']} (ID: {student['student_id']})")
                    print(f"    Courses: {len(student['courses'])}")
                    print(f"    GPA: {student['weighted_gpa']:.2f}")
                else:
                    print(f"\n Student {target_student} not found")
            except ValueError:
                print("\n Invalid ID!")

        elif choice =="4":
            display_students()
        elif choice =="5":
            calculate_average_GPA()
        elif choice == "6":
            sort_students_by_GPA()
        elif choice =="7":
            add_course_to_student()
        elif choice =="8":
            find_min_max()
        elif choice == "9":
            calculate_median()    
        elif choice == "10":
            sort_students_by_grade()
        elif choice == "11":
            class_average_grade() 
        elif choice == "12":
            grade_distribution()           
        else:
            print("GOODBYE!!")
            break

if __name__ == "__main__":   
    main()



        

