import pandas as pd
import numpy as np
import os
import re
from decimal import Decimal, ROUND_HALF_UP
import json


def read_config():
    with open('config.json') as f:
        config = json.load(f)
        path = config['path_submission']
        if path == 'cwd':
            config['path_submission'] = os.getcwd()
    return config


def write_config(**config2update):
    config_old = read_config()
    print('/' * 100)
    print(config_old)
    print(config2update)
    print('/' * 100)
    # When the same key is in both dict, the second dict's value for the key is prioritised
    config_new = {**config_old, **config2update}
    with open('./config.json', 'w') as f:
        json.dump(config_new, f, indent=4)


def df_add_class_str(s):
    """
    Apply to marksheet df to make the table cells scrollable for 'Feedback' column.
    """
    col = 'Feedback'
    return f'__{col.lower()}__' + str(s)


def df_scrollable(df):
    """
    Make cells in the column scrollable by adding class attribute to <td> tags
    Ref:
        https://stackoverflow.com/questions/65442733/is-it-possible-to-add-a-class-or-id-to-a-specific-column-td-when-using-python
    Params:
        Dataframe that are converted to html table
    Returns:
        HTML
    """
    _df = df.copy()
    col = 'Feedback'
    if col in _df.columns:
        _df[col] = _df[col].apply(df_add_class_str)
        str_html = ''
        html_lines = list(map(lambda line: line.replace(f'<td>__{col.lower()}__', f'<td>\n<div class="{col.lower()}">').replace('</td>', '</div>\n</td>') if f'__{col.lower()}__' in line else line, _df.to_html().split('\n')))
        for line in html_lines:
            str_html += line + '\n'
    else:
        str_html = _df.to_html()
    # "corner" class for highest 'z-index'
    str_html = str_html.replace('<th></th>', '<th class="corner" style="z-index: 2;position: sticky;top: 0px;left: 0px;"></th>')
    # Remove unnecessary strings
    for i in {'NaN', 'nan', f'__{col.lower()}__'}:
        str_html = str_html.replace(i, '')
    return str_html


"""
For Marking Criteria Editing Page
"""


def load_csv(path, **kwargs):
    mode = kwargs.pop('mode', 'marking_criteria')
    if mode == 'marking_criteria':
        path_cps = os.path.join(path, 'checkpoints.csv')
        path_gpp = os.path.join(path, 'good_programming_practice.csv')
        # If csv files do not exist
        if os.path.exists(path_cps):
            df_cps = pd.read_csv(path_cps, index_col=0)
        else:
            df_cps = pd.DataFrame()
        if os.path.exists(path_gpp):
            df_gpp = pd.read_csv(path_gpp, index_col=0)
        else:
            df_gpp = pd.DataFrame()
        return df_cps, df_gpp
    elif mode == 'marksheet':
        # If csv files do not exist
        if os.path.exists(path):
            df_ms = pd.read_csv(path, index_col=0)
        else:
            df_ms = pd.DataFrame()
        return df_ms


def save_csv(*args):
    if len(args) == 3:
        df_cps, df_gpp, path_asset = args[0], args[1], args[2]
        path_cps = os.path.join(path_asset, 'checkpoints.csv')
        path_gpp = os.path.join(path_asset, 'good_programming_practice.csv')
        df_cps.to_csv(path_cps)
        df_gpp.to_csv(path_gpp)
    elif len(args) == 2:
        df_ms, path_ms = args[0], args[1]
        df_ms.to_csv(path_ms)


def get_files(path):
    '''
    List files under the given path
    '''
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return sorted(files)


def get_folders(path):
    '''
    List folders under the given path
    '''
    folders = [f for f in os.listdir(path) if os.path.isdir(os.path.join(path, f))]
    return sorted(folders)


def get_marks(criteria):
    pattern_mark = r'([\W\w]+)\s(\[[0-9]+\])'
    txt, mark = re.findall(pattern_mark, criteria)[0]
    return txt, mark[1::-2]


class MarkingCriteria:
    def __init__(self, path_submission):
        self.path_submission = path_submission
        self._df_cps, self._df_gpp = load_csv(self.path_submission, mode='marking_criteria')

    @property
    def term(self):
        return self._term

    @property
    def hw(self):
        return self._hw

    @term.setter
    def term(self, value):
        if value in [1, 2, 3]:
            pass
        else:
            value = 1
        self._term = value

    @hw.setter
    def hw(self, value):
        if type(value):
            pass
        else:
            value = 1
        self._term = value

    @property
    def df_cps(self):
        return self._df_cps

    @property
    def df_gpp(self):
        return self._df_gpp

    @df_cps.setter
    def df_cps(self, df):
        self._df_cps = df

    @df_gpp.setter
    def df_gpp(self, df):
        self._df_gpp = df

    def df_add_cols(self, colname):
        if colname not in self.df_cps.columns.values:
            self.df_cps[str(colname)] = np.nan
        if colname not in self.df_gpp.columns.values:
            self.df_gpp[str(colname)] = np.nan

    def df_del_cols(self, colname):
        if colname in self.df_cps.columns.values:
            self.df_cps.drop(columns=[str(colname)], inplace=True)
        if colname in self.df_gpp.columns.values:
            self.df_gpp.drop(columns=[str(colname)], inplace=True)


class MarkSheet(MarkingCriteria):
    def __init__(self, path_submission):
        super().__init__(path_submission)
        self._path_marksheet = os.path.join(self.path_submission, 'T1HW1_marksheet.csv')
        self.df_ms = load_csv(self._path_marksheet, mode='marksheet')

    def get_marksheet(self, term, hw, sub_ids):
        if not os.path.exists(self._path_marksheet):
            lis_cps = [
                f'checkpoint {e} [{e + 1}]' if (isinstance(i, (int, float)) and np.isnan(i)) else i
                for e, i in enumerate(self.df_cps[f'T{term}HW{hw}'].values)
            ]
            lis_gpp = [
                f'good programming practice{e} [{e + 1}]' if (isinstance(i, (int, float)) and np.isnan(i)) else i
                for e, i in enumerate(self.df_gpp[f'T{term}HW{hw}'].values)
            ]
            cols = lis_cps + lis_gpp + ['Feedback']
            self.df_ms = pd.DataFrame(columns=cols, index=sub_ids)
            self.df_ms['Feedback'] = ''
        else:
            self.d_ms = load_csv(self._path_marksheet, mode='marksheet')

    @property
    def path_marksheet(self):
        return self._path_marksheet

    @path_marksheet.setter
    def path_marksheet(self, value):
        self._path_marksheet = value
        self.df_ms = load_csv(self._path_marksheet, mode='marksheet')


"""
For Marking Page
"""


def string2list(string, splitby=':::'):
    return string.split(splitby)


def list2string(lis, splitby=':::'):
    return splitby.join(lis)


def list2string_routine(submission_ids: list, ms: MarkSheet):
    # Convert the submission IDs list into a string
    sub_ids_str = list2string(submission_ids)
    # Do not show 'Feedback' in the drop-down menue
    lis_points = list(ms.df_ms.columns.values)
    if 'Feedback' in lis_points:
        lis_points.remove('Feedback')
    # Convert the checkpoints list assocciated with the homework into a string
    points_str = list2string(lis_points)
    return sub_ids_str, points_str


"""
Markdown Report Generation
"""


def get_dataframes(df_mark, term, hw, marking_criteria):
    '''
    Divide the DataFrame into df for marks for code, good perogramming practice, and feedbacks
    '''
    list_checkpoints = marking_criteria.df_cps[f'T{term}HW{hw}']
    list_gpp = marking_criteria.df_gpp[f'T{term}HW{hw}']
    # Main python code marks
    df_checkpoints = df_mark[df_mark.columns.intersection(list_checkpoints)]
    # Good Programming Practice mark
    df_gpp = df_mark[df_mark.columns.intersection(list_gpp)]
    df_feedbacks = df_mark['Feedback']
    return df_checkpoints, df_gpp, df_feedbacks


def generate_summary(submission_id, df_marksheet, term, hw, marking_criteria, assessor, template_head, template_common):
    if submission_id not in df_marksheet.index:
        return 'submission id is not valid'
    else:
        '''
        1. Divide the spreadsheet into coding mark, good programming practice mark, feedback dataframes
        '''
        df_checkpoints, df_gpp, df_feedbacks = get_dataframes(df_marksheet, term, hw, marking_criteria)

        # If empty dataframe, return warnings
        if any([df_checkpoints.empty, df_gpp.empty]):
            return None

        '''
        2. Calc. Subtotal mark, good programming practice mark (rounded to 1st decimal place by default)
        '''
        subtotal = df_checkpoints.loc[submission_id].sum()
        gpp_mean = df_gpp.loc[submission_id].mean()
        # Round the mark to 1st d.p.
        gpp_mean = float(Decimal(str(gpp_mean)).quantize(Decimal('0.1'), ROUND_HALF_UP))
        # Round the total mark to 1st d.p.
        mark_total = float(Decimal(str(subtotal + gpp_mean)).quantize(Decimal('0.1'), ROUND_HALF_UP))

        '''
        3. Generate the markdown script for feedback, tables of marks in each section
        '''
        # If the feedbnack is not empty, add feedbacks as bulletpoints
        list_fb = [fb for fb in str(df_feedbacks.loc[submission_id]).split('///') if type(df_feedbacks.loc[submission_id]) == str]
        # '{-}' is added to avoid previent index from being added when converted to a pdf
        feedback = '## Summary {-}\n\n'
        feedback += f'{template_head}\n\n'
        feedback += '**Frequently seen mistakes**: \n\n'
        feedback += f'{template_common}\n\n'
        feedback += '**Feedbacks**:\n\n'
        for fb in list_fb:
            feedback += f'- {fb}\n\n'
        feedback += '\n'

        list_cp_loaded = list(df_checkpoints.loc[submission_id].index)
        list_cp = [re.split(r'\s(\[\d\])', cp)[0] for cp in list_cp_loaded]
        list_cp_fullmark = [int(re.sub(r"\D", "", cp.split(' ')[-1])) for cp in list_cp_loaded]
        list_cp_mark = df_checkpoints.loc[submission_id].values

        list_gpp_loaded = list(df_gpp.loc[submission_id].index)
        list_gpp = [re.split(r'\s(\[\d\])', gpp)[0] for gpp in list_gpp_loaded]
        list_gpp_fullmark = [int(re.sub(r"\D", "", gpp.split(' ')[-1])) for gpp in list_gpp_loaded]
        print('|' * 100)
        print(df_checkpoints)
        print(list_gpp_fullmark)
        list_gpp_mark = df_gpp.loc[submission_id].values

        table_cp = '### Correctly Functioning Code {-}\n\n|Check Point|Mark|\n|---|---|\n'
        for cp, mark, markfull in zip(list_cp, list_cp_mark, list_cp_fullmark):
            table_cp += f"|{cp}|{mark} / {markfull}|\n"
        table_cp += f"|\\textcolor{{blue}}{{Sub Total}}|\\textcolor{{blue}}{{{subtotal} / {sum(list_cp_fullmark)}}}|"

        table_gpp = '### Good Programming Practice {-}\n\n|Check Point| Mark|\n|---|---|\n'
        for gpp, mark, markfull in zip(list_gpp, list_gpp_mark, list_gpp_fullmark):
            table_gpp += f"|{gpp}|{mark} / {markfull}|\n"
        table_gpp += f"|\\textcolor{{blue}}{{Average}}|\\textcolor{{blue}}{{{gpp_mean} / {int(sum(list_gpp_fullmark) / len(list_gpp_fullmark))}}}|"

        markdown = feedback + table_cp + '\n\n' + table_gpp
        full_mark_overall = sum(list_gpp_fullmark) / len(list_gpp_fullmark) + sum(list_cp_fullmark)
        markdown += f'\n\n**Total \\textcolor{{red}}{{{mark_total} / {full_mark_overall}}}**\n\n(Assessor: {assessor})'
        return markdown
