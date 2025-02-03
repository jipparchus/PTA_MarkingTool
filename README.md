# PTA_MarkingTool


A tool to $\color{red}{\textsf{speed up marking}}$ & to generate $\color{blue}{\textsf{summary feedback report}}$ for each submission. 

<h2>Motivations</h2>

I want to make the workflow for my Python coursework marking job more efficient. While I was marking submissions, some factors prevented me from spending more time on writing productive and encouraging feedback, for example:

- It was time-consuming to **travel between Excel mark sheets, notepad, and Jupyter Notebook**.
- Extra attention must be paid to the **manual selection of cells** in the mark sheet.
- Feedback and common mistakes found had to be kept in the notepad app.
- Manual writing of the summary report did not guarantee **consistency** in the format. Copying, pasting and modifying the form looked inefficient.

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



## $\color{green}{\textsf{Example of Summary Report}}$

### Summary {-}

**Well done all who submitted the homework!!**

Much less `X not defined` errors this time!! Good work!


**Frequently seen mistakes**: 

- Strange indentations in code cells.

- Packing all the script in a single code cell.


**Feedbacks**:

- feedback 1

- feedback 2


### Correctly Functioning Code {-}

|Check Point|Mark|
|---|---|
|Check Point 1|1.0 / 1|
|Check Point 2|3.0 / 3|
|Check Point 3|3.0 / 5|
|Check Point 4|3.0 / 3|
|Check Point 5|1.0 / 1|
|Check Point 6|1.0 / 1|
|Check Point 7|1.0 / 1|
|$\color{blue}{\textsf{Sub Total}}$|$\color{blue}{\textsf{13.0}}$ / $\color{blue}{\textsf{15}}$|

### Good Programming Practice {-}

|Check Point| Mark|
|---|---|
|Good Programming Practice 1|5.0 / 5|
|Good Programming Practice 2|5.0 / 5|
|Good Programming Practice 3|5.0 / 5|
|Good Programming Practice 4|5.0 / 5|
|Good Programming Practice 5|5.0 / 5|
|$\color{blue}{\textsf{Average}}$| 	$\color{blue}{\textsf{5.0}}$ / $\color{blue}{\textsf{5}}$|

**Total $\color{red}{\textsf{18.0}}$ / $\color{red}{\textsf{20.0}}$**

(Assessor: QQ)




<h2>How to Use</h2>

**Initial Seting Up**

1. Download the project to your local machine by 'Code' > 'Download ZIP'. Unzip the folder
2. Rename `config.json.defo` ➡️ `config.json`.
3. Open the terminal/command prompt and move to the folder location.
4. Activate the virtual environment if necessary, then `python run.py`.
5. If no error messages, 'ctrl' + 'click' the link appears (e.g. http://127.0.0.1:5000) on the terminal/command prompt.
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

<video src="https://github.com/user-attachments/assets/0d52a294-a646-4707-b616-65f3343203de" controls playsinline autoplay loop muted width="500"></video>

**Marking Process (NEED TO BE COMPLETED)**

There are 3 tabs for the application.
1. Marking criteria editor page

<video src="https://github.com/user-attachments/assets/0bac0979-e54e-4440-9fad-a40e69647eea" controls playsinline autoplay loop muted width="500"></video>

2. Markingsheet editing page **(✅"\_\_feedback\_\_" bug has been removed )**

Feedbacks will be shown with bullet points by default. Please change lines twice between feedbacks. The same rules apply for the 'Common Mistakes' section. You can leave the section empty if there is nothing to mention.

<video src="https://github.com/user-attachments/assets/bf32265c-b2c1-454f-bec3-3f23474c58b6" controls playsinline autoplay loop muted width="500"></video>


3. Summary report generation page **(✅"\_\_feedback\_\_" bug has been removed )**

- Select a homework, confirm the submission ID, then press 'Generate Report' to generate a markdown report. Please edit the template in any ways you like!
- The style of markdown coloured text is just tested for my environment only. The default set of the style for colour text may not work for your environment. Please try different styles and editing the config file if required, then convert the notebook to PDF to see if it works.
- Copy the markdown report and paste that on the submitted .ipynb and convert to .pdf.
- Conversion command of .ipynb to .pdf may not work for your environment.

<video src="https://github.com/user-attachments/assets/87f6a76c-4700-45a3-840a-a60005497ed4" controls playsinline autoplay loop muted width="500"></video>

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
  - flask-socketio (pip)
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
	├── HW1
	│   ├── submission_id1
	│   │   └── File submissions
	│   │       ├── xxx.ipynb
	│   │       └── data.csv
	│   ├── submission_id2
	│   └── ...
	├── HW2
	├── ...
	├── checkpoints.csv                [ AUTO-GENERATED ]
	├── good_programming_practice.csv  [ AUTO-GENERATED ]
	├── HW1_marksheet.csv              [ AUTO-GENERATED ]
	└── HW2_marksheet.csv              [ AUTO-GENERATED ]
```

<h2>Known Issues</h2>

So far, the application does the minimum job and is planned to be shared with my colleagues.  
- Demo videos are out of dated (Some bugs have ben fixed and new functionalities have been implemented.)
- There is not enough README to show how to use the app.
The order of the index in marking criteria is not ascending but just in the order of added timing.
- When marking criteria is edited after the mark sheet is modified, some checkpoints disappear from the mark sheet.
- Want to reduce the number of buttons by using JavaScript

