# PTA_MarkingTool
A tool to speed-up marking &amp; to generate markdown summary feedback for each submission


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
- numpy
- pandas
- flask
- markdown

**Seting Up the App**

1. Download the project to your local machine by 'Code' > 'Download ZIP'. Unzip the foilder
2. Open terminal / command prompt and move to the folder location.
3. Do `Python run.py`. If no error messages, 'ctrl' + 'click' the link apear on the terminal / command prompt.
4. Make sure the path to the submission folders is correct.

**How to Use**

There are 3 tabs for the application.
1. Marking c riteria editor page
2. Markingsheet editing page
3. Markdown summary of marks and feedbacks generation page
