# Teaching assessment webapp

This was my final project for cs50's web programming with python and javascript course. [Demonstration Video](https://youtu.be/8nfCOiSet1s).

## Distinctiveness and Complexity

This project is a teaching assessment webapp which has 3 ***types of users***; teachers, students, and admin. Each user can not see the other ***user type***'s pages. Teacher and student have different register and login routes. Each user's experience with website will be described bellow:

### Student

- Each student can register by specifying their ID number; only if the ID is in the **IDNumbers** model, they can register.
- After logging in, the user can see their name, see all available forms, can purchase prizes, and can change their password
- By going to assessment *forms tab*;
  - The user can choose any form (associated with a teacher, their picture, the subject, and the academic year).
  - By clicking a form, they can answer its questions and submit
  - Only students that a form is for, can view the form
  - By answering the form, it will not show in their *forms tab* anymore
  - The user's score will increase by answering each form
- By going to *prizes tab*;
  - They can see their current score
  - Can see all bought prizes and copy the code
  - Can buy a new prize (If already bought: error)
  - Having **prizes** and **score** is a way to create incentive for students to answer the questions and visit the website

### Teacher/TA

- After logging in, the user can see their name (If they're TA: see their supervisors), subjects thought in the active academic year, see each academic years results, and can change their password
- By going to *results tab*;
  - The user can choose the academic year to see the results of
  - Results will be shown as described bellow:
    - First a table of all subjects of that year and number of students answered
    - For each subject the answers logged in **FormAnswerS** model will be filtered by subject
    - For closed questions the number of respondents for each value will be shown in a table and a diagram
    - For open questions all answers will be shown under the question text 

### Admin

- Can import student ID numbers using django shell and csv
- Add new academic years (specifying its 'state'; active or not)
- Can add a form (Name of this model is **Course**) 
  - Fields of this form are written below:
    - Students which this form will be shown for
    - Students that have not answered this form
    - **Score** of answering this form
    - Teacher associated with this form
    - Specifying whether the teacher is a teacher assistant and if they are, who is their supervisor in this specific form
    - What is the coursename associated with this form
    - For which academic year this form is
    - The formsample associated with this form
- Can make a new **FormSample**
  - A formsample can be used for multiple forms without the need to rewrite each question
  - Fields of this form are written below:
    - Name and description of this formsample
    - All questions associated with this formsample
- Can add **Questions**
  - Each question can have open or closed answers
  - Fields of this form are written below:
    - Question text which stores the question itself
    - Type of question: currently: *OPEN* or *CLOSE*
    - If is *CLOSE*: what are possible answer values (and number of values/radio buttons)
- Can add **PrizeNames**
  - Each students can earn a prize by spending their **Scores**!
  - By buying a prize, a new log of this prize is added to **PrizesGot**.
  - Fields of this form are written below:
    - Name and description of this prize
    - Score needed to earn this prize

## File and folder contents

Each file's contents are explained in this tree; showing directories and files. 

```
.
├── ...
├── assessment_app
│   ├── ...
│   ├── models.py
│   ├── static
│   │   └── assessment_app
│   │       ├── css
│   │       │   ├── ...
│   │       │   └── 🌄 styles.scss >>> styles defined here and for responsiveness
│   │       ├── img
│   │       │   └── ...
│   │       └── js
│   │           ├── ...
│   │           ├── 🎆 change_password.js >>> front-end for changing passwords and fetching from api
│   │           ├── 🎆 control.js >>> control of purchasing and showing purchased prizes
│   │           ├── 🎆 cookie_alert.js >>> function for getting cookies and alerting user
│   │           └── 🎆 results.js >>> showing and fetching results of each academic year results
│   ├── templates
│   │   └── assessment_app
│   │       ├── 🦴 errors.html >>> html for showing errors
│   │       ├── 🦴 form.html >>> html for showing each form
│   │       ├── 🦴 index.html >>> html for index of website
│   │       ├── 🦴 layout.html >>> layout of all html files
│   │       ├── 🦴 login_s.html >>> html for login page of students
│   │       ├── 🦴 login_t.html >>> html for login page of teachers
│   │       ├── 🦴 register_s.html >>> html for register page of students
│   │       ├── 🦴 register_t.html >>> html for register page of teachers
│   │       ├── 🦴 student.html >>> html for student user profile
│   │       └── 🦴 teacher.html >>> html for teacher user profile
│   ├── 🔗 urls.py >>> url paths and api defined here
│   └── ⚙️ views.py >>> what each url and api path is going to do
├── 🗒️ idimport.csv >>> example list of idnumbers
└── 🗒️ idimport.py >>> idnumber can be imported by pasting the file's content in django shell
```

## How to run the app

Install django. 

```
..\> pip install django
```

Then run django server.

```
..\> py manage.py runserver
```

Go to the development server at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)!

## Other info

I wrote the website template in Farsi. You can change the language in chrome browser by write clicking in page and choosing **Translate to English** option.

All example user's passwords is 12345. 

Teacher example usernames: [skhedri, gakbri]

Student example usernames: [0013458233, 0013458232]

DjangoAdmin username and pass: [admin, admin]