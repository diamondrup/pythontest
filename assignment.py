class User:
    def __init__(self, username, password):
        self.username=username
        self.password=password
        self.login_attempts=0

    def login(self):
        if self.login_attempts>=3:
            print("Try again")
            return False
        username = input("Enter username: ")
        password = input("Enter password: ")
        if self.username == username and self.password == password:
            print("logged in successfully")
            self.login_attempts = 0
            return True
        else:
            self.login_attempts += 1
            print("Invalid username or password")
            return False

    def passwordschan(self):
        new_password = input("Enter new password:")
        self.password = new_password
        print("Password changed successfully")


class Admin(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.lecturers = {}
        self.exam_personnel = {}
        self.subjects = {}

    def add_lecturer(self):
        username = input("Enter lecturer username: ")
        password = input("Enter lecturer password: ")
        profile = {
            'name': input("Enter name: "),
            'address': input("Enter address: "),
            'contact_number': input("Enter contact number: ")
        }
        self.lecturers[username] = {'password': password, 'profile': profile}
        print(f"added successfully")

    def delete_user(self):
        username = input("Enter username to delete: ")
        user_type = input("Enter which you want to delete 1 for lecturer a 2 for exam_personnel: ")
        if user_type == "1":
            if username in self.lecturers:
                del self.lecturers[username]
                print(f"Lecturer {username} deleted successfully")
            else:
                print(f"Lecturer {username} not found")
        elif user_type == "2":
            if username in self.exam_personnel:
                del self.exam_personnel[username]
                print(f"Exam personnel {username} deleted successfully")
            else:
                print(f"Exam personnel {username} not found")

    def update_lecturer_profile(self):
        username = input("Enter lecturer username: ")
        if username in self.lecturers:
            profile = {
                'dob': input("Enter date of birth: "),
                'address': input("Enter address: "),
                'email_address': input("Enter email address: "),
                'age': input("Enter age: "),
                'citizenship': input("Enter citizenship: "),
                'ID': input("Enter ID: "),
                'contact_number': input("Enter contact number: ")
            }
            self.lecturers[username]['profile'].update(profile)
            print(f"Profile of {username} updated successfully")
        else:
            print(f"Lecturer {username} not found")

    def add_subject(self):
        subject_name = input("Enter subject name: ")
        topics = input("Enter topic: ").split(',')
        if len(topics) >= 3:
            self.subjects[subject_name] = topics
            print(f"Subject {subject_name} with topics {topics} added successfully")
        else:
            print("minimum subject required 3 subject")


class Lecturer(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.questions = {}

    def add_question(self):
        subject = input("Enter subject: ")
        topic = input("Enter topic: ")
        question = input("Enter question: ")
        answer = input("Enter answer: ")
        if subject not in self.questions:
            self.questions[subject] = {}
        if topic not in self.questions[subject]:
            self.questions[subject][topic] = []
        self.questions[subject][topic].append({'question': question, 'answer': answer})
        print(f"Question added to {subject} - {topic} successfully")

    def update_question(self):
        subject = input("Enter subject: ")
        topic = input("Enter topic: ")
        question_index = int(input("Enter question index: "))
        try:
            new_question = input("Enter new question: ")
            new_answer = input("Enter new answer: ")
            self.questions[subject][topic][question_index] = {'question': new_question, 'answer': new_answer}
            print(f"Question in {subject} - {topic} updated successfully")
        except IndexError:
            print("Invalid question index")
        except KeyError:
            print("Invalid subject or topic")

    def view_questions(self):
        subject = input("Enter subject: ")
        topic = input("Enter topic: ")
        try:
            questions = self.questions[subject][topic]
            for i, q in enumerate(questions):
                print(f"Q{i+1}: {q['question']} - A: {q['answer']}")
        except KeyError:
            print("Invalid subject or topic")


class ExamPersonnel(User):
    def __init__(self, username, password):
        super().__init__(username, password)
        self.exam_papers = {'Set 1': {'Section A': [], 'Section B': []},
                            'Set 2': {'Section A': [], 'Section B': []}}

    def add_question_to_exam(self):
        set_name = input("Enter exam set name: ")
        section = input("Enter section: ")
        question = input("Enter question: ")
        if set_name in self.exam_papers and section in self.exam_papers[set_name]:
            self.exam_papers[set_name][section].append(question)
            print(f"Question added to {set_name} - {section} successfully")
        else:
            print("Incorrect exam set or section")

    def view_exam_paper(self):
        set_name = input("Enter exam set name: ")
        if set_name in self.exam_papers:
            print(f"Exam Paper {set_name}:")
            for section, questions in self.exam_papers[set_name].items():
                print(f"{section}:")
                for q in questions:
                    print(f"    {q}")
        else:
            print("Invalid exam set")


admin_username = 'admin'
admin_password = 'admin123'
admin = Admin(admin_username, admin_password)

if admin.login():
    while True:
        print("\nAdmin Menu:")
        print("1. Add Lecturer")
        print("2. Delete User")
        print("3. Update Lecturer Profile")
        print("4. Add Subject")
        print("5. Manage Lecturer")
        print("6. Manage Exam Personnel")
        print("7. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            admin.add_lecturer()
        elif choice == '2':
            admin.delete_user()
        elif choice == '3':
            admin.update_lecturer_profile()
        elif choice == '4':
            admin.add_subject()
        elif choice == '5':
            lecturer_username = input("Enter lecturer username: ")
            if lecturer_username in admin.lecturers:
                lecturer = Lecturer(lecturer_username, admin.lecturers[lecturer_username]['password'])
                if lecturer.login():
                    while True:
                        print("\nLecturer Menu:")
                        print("1. Add Question")
                        print("2. Update Question")
                        print("3. View Questions")
                        print("4. Change Password")
                        print("5. Exit")
                        lecturer_choice = input("Enter choice: ")
                        if lecturer_choice == '1':
                            lecturer.add_question()
                        elif lecturer_choice == '2':
                            lecturer.update_question()
                        elif lecturer_choice == '3':
                            lecturer.view_questions()
                        elif lecturer_choice == '4':
                            lecturer.passwordschan()
                        elif lecturer_choice == '5':
                            break
                        else:
                            print("Invalid choice")
            else:
                print("Lecturer not found")
        elif choice == '6':
            exam_personnel_username = input("Enter exam personnel username: ")
            if exam_personnel_username in admin.exam_personnel:
                exam_personnel = ExamPersonnel(exam_personnel_username, admin.exam_personnel[exam_personnel_username]['password'])
                if exam_personnel.login():
                    while True:
                        print("\nExam Personnel Menu:")
                        print("1. Add Question to Exam Paper")
                        print("2. View Exam Paper")
                        print("3. Change Password")
                        print("4. Exit")
                        exam_personnel_choice = input("Enter choice:")
                        if exam_personnel_choice == '1':
                            exam_personnel.add_question_to_exam()
                        elif exam_personnel_choice == '2':
                            exam_personnel.view_exam_paper()
                        elif exam_personnel_choice == '3':
                            exam_personnel.passwordschan()
                        elif exam_personnel_choice == '4':
                            break
                        else:
                            print("Please try again")
            else:
                print("Exam personnel not found")
        elif choice == '7':
            break
        else:
            print("Please try again")
else:
    print("Login failed")
