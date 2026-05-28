import sqlite3
DBNAME = "university.db"

def init_db():
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER,
                major TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_name TEXT NOT NULL,
                instructor TEXT
            )
        ''')
        
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS student_courses (
                student_id INTEGER,
                course_id INTEGER,
                PRIMARY KEY (student_id, course_id),
                FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE,
                FOREIGN KEY (course_id) REFERENCES courses (course_id) ON DELETE CASCADE
            )
        ''')
        conn.commit()

def execute_query(qwery, params = ()):
    with sqlite3.connect(DBNAME) as conn:
        cursor = conn.cursor()
        cursor.execute(qwery, params)
        conn.commit()
        return cursor.fetchall()

def main():
    init_db()
    
    while True:
        print("\n--- Меню Університету ---")
        print("1. Додати нового студента")
        print("2. Додати новий курс")
        print("3. Показати список студентів")
        print("4. Показати список курсів")
        print("5. Зареєструвати студента на курс")
        print("6. Показати студентів на конкретному курсі")
        print("7. Вийти")
        
        choice = input("\nОберіть опцію (1-7): ")
        
        if choice == "1":
           
            name = input("Введіть ім'я студента: ")
            age = int(input("Введіть вік студента: "))
            major = input("Введіть спеціальність (major): ")
            execute_query('INSERT INTO students (name, age, major) VALUES (?, ?, ?)', (name, age, major))
            print(f"Студента {name} успішно додано!")
            
        elif choice == "2":
            
            course_name = input("Введіть назву курсу: ")
            instructor = input("Введіть ім'я викладача: ")
            execute_query('INSERT INTO courses (course_name, instructor) VALUES (?, ?)', (course_name, instructor))
            print(f"Курс {course_name} успішно додано!")
            
        elif choice == "3":
           
            students = execute_query('SELECT * FROM students')
            print("\n--- Список студентів ---")
            for student in students:
                print(f"ID: {student[0]} | Ім'я: {student[1]} | Вік: {student[2]} | Спеціальність: {student[3]}")
                
        elif choice == "4":
            
            courses = execute_query('SELECT * FROM courses')
            print("\n--- Список курсів ---")
            for course in courses:
                print(f"ID: {course[0]} | Назва: {course[1]} | Викладач: {course[2]}")
                
        elif choice == "5":
            
            student_id = int(input("Введіть ID студента: "))
            course_id = int(input("Введіть ID курсу: "))
            try:
                execute_query('INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
                print("Студента успішно зареєстровано на курс!")
            except sqlite3.IntegrityError:
                print("Помилка: Студент вже зареєстрований на цей курс або введено невірні ID.")
                
        elif choice == "6":
           
            course_id = int(input("Введіть ID курсу для перегляду студентів: "))
            query = '''
                SELECT students.id, students.name 
                FROM students 
                JOIN student_courses ON students.id = student_courses.student_id
                WHERE student_courses.course_id = ?
            '''
            students_in_course = execute_query(query, (course_id,))
            
            print(f"\n--- Студенти на курсі з ID {course_id} ---")
            if students_in_course:
                for student in students_in_course:
                    print(f"ID: {student[0]} | Ім'я: {student[1]}")
            else:
                print("На цей курс ще не зареєстровано жодного студента.")
                
        elif choice == "7":
            print("Вихід з програми. До побачення!")
            print('print("https://github.com/ArTmIx99/project2")')
            break
            
        else:
            print("Некоректний вибір. Будь ласка, введіть число від 1 до 7.")

if __name__ == "__main__":
    main()
    