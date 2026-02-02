import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_database",
        use_pure=True
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print("Database Connection Error:", err)
    exit()


def calculate_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 75:
        return 'B'
    elif marks >= 60:
        return 'C'
    elif marks >= 40:
        return 'D'
    else:
        return 'F'


def add_student():
    try:
        id = int(input("Enter ID: "))
        name = input("Enter Name: ")
        course = input("Enter Course: ")
        marks = int(input("Enter Marks (0-100): "))

        if marks < 0 or marks > 100:
            print("Marks must be between 0 and 100")
            return

        grade = calculate_grade(marks)

        sql = "INSERT INTO student_record VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id, name, course, marks, grade))
        conn.commit()
        print("Student Added Successfully")

    except mysql.connector.Error as err:
        print("Error:", err)
    except ValueError:
        print("Invalid Input")


def view_students():
    cursor.execute("SELECT * FROM student_record")
    data = cursor.fetchall()

    if not data:
        print("No records found")
    else:
        print("\nStudent Records:")
        for row in data:
            print(f"ID:{row[0]} | Name:{row[1]} | Course:{row[2]} | Marks:{row[3]} | Grade:{row[4]}")


def search_student():
    choice = input("Search by (1) ID or (2) Name: ")

    if choice == '1':
        id = int(input("Enter ID: "))
        cursor.execute("SELECT * FROM student_record WHERE id=%s", (id,))
    elif choice == '2':
        name = input("Enter Name: ")
        cursor.execute("SELECT * FROM student_record WHERE name LIKE %s", (name+'%',))
    else:
        print("Invalid choice")
        return

    data = cursor.fetchall()
    if data:
        for row in data:
            print(row)
    else:
        print("Student not found")


def update_marks():
    try:
        id = int(input("Enter Student ID: "))
        marks = int(input("Enter New Marks: "))

        grade = calculate_grade(marks)

        sql = "UPDATE student_record SET marks=%s, grade=%s WHERE id=%s"
        cursor.execute(sql, (marks, grade, id))
        conn.commit()

        if cursor.rowcount == 0:
            print("Student not found")
        else:
            print("Marks Updated Successfully")

    except ValueError:
        print("Invalid Input")


def update_details():
    id = int(input("Enter ID: "))
    name = input("Enter New Name: ")
    course = input("Enter New Course: ")

    sql = "UPDATE student_record SET name=%s, course=%s WHERE id=%s"
    cursor.execute(sql, (name, course, id))
    conn.commit()

    if cursor.rowcount == 0:
        print("Student not found")
    else:
        print("Details Updated")


def delete_student():
    id = int(input("Enter Student ID: "))
    cursor.execute("DELETE FROM student_record WHERE id=%s", (id,))
    conn.commit()

    if cursor.rowcount == 0:
        print("Student not found")
    else:
        print("Student Deleted Successfully")


def topper():
    cursor.execute("SELECT * FROM student_record ORDER BY marks DESC LIMIT 1")
    data = cursor.fetchone()
    if data:
        print("Topper:", data)


def average_marks():
    cursor.execute("SELECT AVG(marks) FROM student_record")
    avg = cursor.fetchone()[0]
    print("Average Marks:", avg)


def failed_students():
    cursor.execute("SELECT * FROM student_record WHERE marks < 40")
    data = cursor.fetchall()

    if data:
        print("Failed Students:")
        for row in data:
            print(row)
    else:
        print("No failed students")


while True:
    print("\nSTUDENT MANAGEMENT SYSTEM")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Marks")
    print("5. Update Details")
    print("6. Delete Student")
    print("7. Topper")
    print("8. Average Marks")
    print("9. Failed Students")
    print("10. Exit")

    choice = input("Enter Choice: ")

    if choice == '1':
        add_student()
    elif choice == '2':
        view_students()
    elif choice == '3':
        search_student()
    elif choice == '4':
        update_marks()
    elif choice == '5':
        update_details()
    elif choice == '6':
        delete_student()
    elif choice == '7':
        topper()
    elif choice == '8':
        average_marks()
    elif choice == '9':
        failed_students()
    elif choice == '10':
        print("Thank You")
        break
    else:
        print("Invalid Choice")

cursor.close()
conn.close()
