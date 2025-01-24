# PTA_MarkingTool


A tool to $\color{red}{\textsf{speed up marking}}$ & to generate $\color{blue}{\textsf{summary feedback report}}$ for each submission. 

<h2>Motivations</h2>

I want to make the workflow for my Python coursework marking job more efficient. While I was marking submissions, some factors prevented me from spending more time on writing productive and encouraging feedback, for example:

- It was time-consuming to **travel between Excel mark sheets, notepad, and Jupyter Notebook**.
- Extra attention must be paid to the **manual selection of cells** in the mark sheet.
- Feedback and common mistakes found had to be kept in the notepad app.
- Manual writing of the summary feedback form did not guarantee **consistency** in the format. Copying, pasting and modifying the form looked inefficient.

<h2>This Application Provides ...</h2>

A marking tool that integrates:

- Marking criteria editor
- Mark sheet editor
- Feedback notes for each submission
- Notepad for frequently seen mistakes
- Feedback report generator

The application works locally. No internet connection is needed for security reasons.

You will need to open only this application, the Jupyter Notebook submitted, and the marking instructions provided by the module leader.

<h3>Points</h3>

- This is designed to minimise the use of keyboard input because this makes the marking process smoother, personally.

- The note-taking area for frequently seen mistakes is oriented in the mark sheet editing tab because they are found during marking, while the note is used to generate the report generation page. 


<h2>How to Use</h2>

**Initial Seting Up**

1. Download the project to your local machine by 'Code' > 'Download ZIP'. Unzip the folder
2. Rename `config.json.defo` ➡️ `config.json`.
3. Open the terminal/command prompt and move to the folder location.
4. Activate the virtual environment if necessary, then `python run.py`.
5. If no error messages, 'ctrl' + 'click' the link appears on the terminal/command prompt.
6. Edit to make sure the path to the submission folders is correct.

```bash
(Env_MarkingTool) C:\Users\QQ\Documents\marking_demo\MarkingTool>python run.py
 * Serving Flask app 'app.app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 126-070-293
```


For the first run, edit the path to the submissions directory & assessor's initials. Click 'Save Change' to save the configurations.


<video src="https://github.com/user-attachments/assets/842c2961-15e1-4600-be47-2548757c0721" controls playsinline autoplay loop muted width="500"></video>

**Marking Process (NEED TO BE COMPLETED)**

There are 3 tabs for the application.
1. Marking criteria editor page


<video src="https://github.com/user-attachments/assets/1f203d72-21be-4a5b-8e34-61482fb627e2" controls playsinline autoplay loop muted width="500"></video>




3. Markingsheet editing page
4. Markdown summary of marks and feedbacks generation page



<h2>Other Information</h2>

**Development Environment**
- Windows 11
- Ubuntu 24.04 LTS

**Dependency**
- Python 3 (Miniconda environment)
  - Flask (conda)
  - Numpy (conda)
  - Pandas (conda)
  - markdown (conda)
- HTML
- CSS
- JavaScript

**Example Filing System**
```
/.../coursework_marking
├── files_for_demonstrators
├── MarkingTool                            [ !!! THIS-APP !!! ]
│   ├── ...
│   └── run.py                             [ !!! USE THIS TO RUN THE APP !!! ]
└── submissions
	├── T1HW1
	│   ├── submission_id1
	│   │   └── File submissions
	│   │       ├── xxx.ipynb
	│   │       └── data.csv
	│   ├── submission_id2
	│   └── ...
	├── T1HW2
	├── ...
	├── checkpoints.csv                [ AUTO-GENERATED ]
	├── good_programming_practice.csv  [ AUTO-GENERATED ]
	├── T1HW1_marksheet.csv            [ AUTO-GENERATED ]
	└── T1HW2_marksheet.csv            [ AUTO-GENERATED ]
```

<h2>Known Issues</h2>

So far, the application does the minimum job and is planned to be shared with my colleagues.  

- There is not enough README to show how to use the app.
The order of the index in marking criteria is not ascending but just in the order of added timing.
- When marking criteria are edited after the mark sheet is edited, some checkpoints disappear from the mark sheet.
- Want to reduce the number of buttons by using JavaScript
- String \__feedback\__ added to modify HTML is left inside the feedback text without being deleted sometimes.
