# Student Grade Calculator

## 📌 Project Description
This project is a Python-based command-line application that dynamically processes student performance. It takes a student's name and marks as input, rigorously validates the data, and utilizes functional logic to return the corresponding grade alongside an encouraging, context-aware message.

---

## 🎯 Objectives
- Implement Python conditional control flow (`if-elif-else`).
- Guarantee data integrity using input validation and `while` loops.
- Architect modular code utilizing Python functions.
- Deliver a robust, user-friendly command-line interface.

---

## 🛠️ Technical Requirements Implemented
- Control Flow: `if-elif-else` statements handle the core grading logic.
- Input Validation: A `while True` loop is implemented to continuously prompt the user until a valid numerical score (0–100) is provided.
- Modularity: Logic is separated into distinct functions (`determine_grade()`, `get_valid_marks()`, and `main()`) for clean architecture.
- Exception Handling: Utilized `try-except` blocks to prevent program crashes when users input non-numeric strings.

---

## 🧮 Grading Logic
The program utilizes the following threshold logic, processed via `if-elif-else` conditions:

| Marks Range | Grade | Feedback Message |
|------------|-------|------------------|
| 90–100 | A | Outstanding! You are at the top of the class! |
| 80–89 | B | Very Good! Keep it up! |
| 70–79 | C | Good effort! A little more practice will get you higher. |
| 60–69 | D | Passed. Consider reviewing the material.  |
| 0–59 | F | Don't give up! Reach out for help...  |

---

## ⚙️ Setup & Installation
1. Install Python on your system
2. Download or clone this repository
3. Open the project folder in your terminal or VS Code
4. Run the program using:
   python personal_intro.py

---

## 📂 Project Files
- `grade_calculator.py` – Main Python program
- `README.md` – Project documentation
- `test_cases.txt` – Test Cases
- `screenshot.png` – Visual proof of successful execution

---

## 📊 Sample Input
Welcome to the Student Grade Calculator

Enter student name: Priya
Enter marks (0-100): 85

## 📊 Result for Sample Input:
Marks: 85/100
Grade: B
Message: Very Good! Keep it up! 

---

## 📚 What I Learned
From this project, I learned how to:
- Encapsulate logic within modular functions, making the codebase cleaner and easier to maintain.
- Implement infinite while loops coupled with try-except blocks to create impenetrable input validation, preventing bad user data from crashing the application.
- Translate real-world business logic (a grading rubric) into sequential if-elif-else structures.
- Organize, document, and upload a structured project to GitHub

