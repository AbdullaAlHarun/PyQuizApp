# README.md — PyQuizApp

## Table of Contents
1. [Project Description](#project-description)  
2. [Team Members](#team-members)  
3. [Usage Instructions](#usage-instructions-install-and-usage)  
   - [Requirements](#requirements)  
   - [Installation](#installation)  
   - [Running Question 1 (JSON Version)](#running-question-1-json-version)  
   - [Running Question 3 (Database Version)](#running-question-3-database-version)  
4. [Additional Libraries Used](#additional-libraries-used)  
5. [Team Member Contributions and Reflection](#team-member-contributions-and-reflection)  
   - [Abdulla Al Harun](#abdulla-al-harun)  
   - [Mostafa Maassou](#mostafa-maassou)  
6. [Working as a Team](#working-as-a-team)  

---

## Project Description
PyQuizApp is a terminal-based quiz program created for the Python & Databases coursework. The first section of the project runs a multiple-choice quiz using the provided `questions.json` file. It loads the questions, displays menus, validates user input, and shows a summary at the end.

The second section extends the quiz to use a MySQL database instead of the JSON file. A database schema is created, the JSON data is imported into MySQL, and the quiz questions are retrieved and displayed using SQL queries.

This project demonstrates working with structured data, input validation, Python functions, SQL schema design, and basic database interaction.

---

## Team Members
- Abdulla Al Harun  
- Mostafa Maassou

---

## Usage Instructions (Install and Usage)

### Requirements
- Python 3.10+
- MySQL Server
- `mysql-connector-python` (required for database version)

### Installation
Clone the repository:
```
git clone https://github.com/AbdullaAlHarun/PyQuizApp.git
```
```
cd PyQuizApp
```

Install the MySQL connector:

```
pip install mysql-connector-python
```

---

### Running Question 1 (JSON Version)
Run the quiz using:

```
python quiz.py
```


### Features include:
- Loads questions from `questions.json`
- Choose a single game, all games, or a random 15-question quiz
- Shuffles question order
- Input validation for A/B/C/D
- Quit anytime with `Q`
- Summary of correct/incorrect answers
- Review of mistakes

---

### Running Question 3 (Database Version)

#### 1. Create the database

```
mysql -u root -p < init.sql
```


#### 2. Import JSON questions into MySQL
```
python question3/import.py
```


#### 3. Run the database version of the quiz
```
python question3/quiz_db.py
```


---

## Additional Libraries Used

### Built-in
- json — reading quiz data  
- random — shuffling and selecting questions  

### External
- mysql.connector — connecting Python to MySQL  

---

## Team Member Contributions and Reflection

### Abdulla Al Harun
**Role in the project:**  
I implemented the JSON-based quiz, including loading data, building the game menu, handling answer input and validation, and generating the final summary. I also structured the project repository, created the MySQL database schema, and wrote the import script to load the JSON data into the database.

**Reflection:**  
While working on the database version, I needed a clear way to represent questions and their answer options. A relevant StackOverflow discussion helped guide my approach to storing multiple-choice options in relational tables:  
https://stackoverflow.com/questions/14740504/the-optimal-way-to-store-multiple-selection-survey-answers-in-a-database  
Testing the import process step-by-step ensured the database matched the original JSON structure and prevented data inconsistencies.

---

### Mostafa Maassou
**Role in the project:**  
I reviewed the database structure, tested the imported data, and verified quiz behavior across both the JSON and database versions. I also contributed to documentation and tested user input edge cases.

**Reflection:**  
I focused on ensuring the program handled invalid input correctly and didn’t break during the quiz flow. A helpful StackOverflow thread clarified how to repeatedly prompt for input until it is valid:  
https://stackoverflow.com/questions/23294658/asking-the-user-for-input-until-they-give-a-valid-response  
This helped me understand user-input loops more clearly and apply them confidently in Python.

---

## Working as a Team
Working as a team allowed us to divide the work effectively while still reviewing each other's progress. Discussing database structure and program flow early helped avoid mistakes and made the final implementation cleaner. Teamwork also made testing faster and improved the overall quality of the project compared to working alone.

---


