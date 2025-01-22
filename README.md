# PTA_MarkingTool
A tool to speed-up marking &amp; to generate markdown summary feedback for each submission


**Expected Filing System**

/xxx/yyy/Submissions
|_T1HW1
|_T1HW2
	|_submission_id1
		|_File submissions
			|_ xxx.ipynb
	|_submission_id2
	|_submission_id3
|_checkpoints.csv
|_good_programming_practice.csv
|_T1HW1_marksheet.csv
|_T1HW2_marksheet.csv


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
