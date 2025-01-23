# PTA_MarkingTool

A tool to $\color{red}{\textsf{speed up marking}}$ & to generate $\color{blue}{\textsf{markdown feedback}}$ for each submission.

**Example Filing System**
```
/.../coursework_marking
├── files_for_demonstrators
├── MarkingTool                        [ !!! THIS-APP !!! ]
|   ├── ...
|   └── run.py                         [ !!! USE THIS TO RUN THE APP !!! ]
└── submissions
	├── T1HW1
	│   ├── submission_id1
	|   |   └── File submissions
	|   |       ├── xxx.ipynb
	|   |       └── data.csv
	│   ├── submission_id2
	|   └── ...
	├── T1HW2
	├── ...
	├── checkpoints.csv                [ AUTO-GENERATED ]
	├── good_programming_practice.csv  [ AUTO-GENERATED ]
	├── T1HW1_marksheet.csv            [ AUTO-GENERATED ]
	└── T1HW2_marksheet.csv            [ AUTO-GENERATED ]
```

**Dependency**
- Python 3
- Numpy
- Pandas
- Flask
- markdown

**Seting Up the App**

1. Download the project to your local machine by 'Code' > 'Download ZIP'. Unzip the folder
2. Rename `config.json.defo` ➡️ `config.json`.
3. Open terminal/command prompt and move to the folder location.
4. Activate virtual environment if necessary, then `python run.py`.
5. If no error messages, 'ctrl' + 'click' the link apear on the terminal/command prompt.
6. Edit sure the path to the submission folders is correct.


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

**How to Use**

	For the first run, edit the path to the submissions directory & assessor's initials. Click 'Save Change' to save the configurations.

There are 3 tabs for the application.
1. Marking criteria editor page
2. Markingsheet editing page
3. Markdown summary of marks and feedbacks generation page
