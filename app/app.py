import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import re
from .utils import save_csv, get_folders, get_marks, MarkingCriteria, MarkSheet, generate_summary, string2list, list2string, list2string_routine, read_config, write_config, df_scrollable
import markdown
from multiprocessing import Process, Queue, cpu_count, current_process, Manager
import subprocess
from queue import Empty
import time

app = Flask(__name__)
socketio = SocketIO(app, async_mode="threading")
config = read_config()
path_sub = config['path_submission']
template_head = config['template_head']
template_common = config['template_common_mistake']


def load_mc():
    path_sub = read_config()['path_submission']
    global mc, ms
    mc = MarkingCriteria(path_sub)
    ms = MarkSheet(path_sub)


load_mc()


def get_form_info(attrs, mode='form_get', **kwargs):
    """
    Params:
        attrs: list of attribute names
        kwargs: attribute whoes defo value need to be modified.
    Return:
        list of values of each attribute
    """
    defo_hw = kwargs.pop('hw', '1')
    defo_cps_idx = kwargs.pop('cps_idx', '0')
    defo_cps_txt = kwargs.pop('cps_txt', 'checkpoint')
    defo_cps_mark = kwargs.pop('cps_mark', '1')
    defo_gpp_idx = kwargs.pop('gpp_idx', '0')
    defo_gpp_txt = kwargs.pop('gpp_txt', 'checkpoint')
    defo_gpp_mark = kwargs.pop('gpp_mark', '1')
    defo_sub_ids_str = kwargs.pop('sub_ids_str', 'submission id')
    defo_points_str = kwargs.pop('points_str', 'checkpoint1 [mark]:::checkpoint2 [mark]')
    defo_sub_id_selected = kwargs.pop('sub_id_selected', 'submission id')
    defo_point_selected = kwargs.pop('point_selected', 'checkpoint [mark]')
    defo_message = kwargs.pop('message', 'No Messages')
    defo_feedback = kwargs.pop('feedback', '')
    defo_feedback_collection = kwargs.pop('feedback_collection', 'feedback 1:::feedback 2')
    defo_mark_int = kwargs.pop('mark_int', '0')
    defo_mark_dec = kwargs.pop('mark_dec', '0')
    defo_summary = kwargs.pop('summary', 'Summary will be generated here')
    defo_template_head = kwargs.pop('template_head', template_head)
    defo_template_common = kwargs.pop('template_common', template_common)
    defo_path_sub = kwargs.pop('path_sub', path_sub)
    defo_assessor = kwargs.pop('path_sub', 'assessor')
    defo_cmode_selected = kwargs.pop('cmode_selected', 'cmode2')

    dict_defo = {
        'hw': defo_hw,
        'cps_idx': defo_cps_idx,
        'cps_txt': defo_cps_txt,
        'cps_mark': defo_cps_mark,
        'gpp_idx': defo_gpp_idx,
        'gpp_txt': defo_gpp_txt,
        'gpp_mark': defo_gpp_mark,
        'sub_ids_str': defo_sub_ids_str,
        'points_str': defo_points_str,
        'sub_id_selected': defo_sub_id_selected,
        'point_selected': defo_point_selected,
        'message': defo_message,
        'feedback': defo_feedback,
        'feedback_collection': defo_feedback_collection,
        'mark_int': defo_mark_int,
        'mark_dec': defo_mark_dec,
        'summary': defo_summary,
        'template_head': defo_template_head,
        'template_common': defo_template_common,
        'path_sub': defo_path_sub,
        'assessor': defo_assessor,
        'cmode_selected': defo_cmode_selected,
    }

    if mode == 'form_get':
        return tuple(request.form.get(attr, dict_defo[attr]) for attr in attrs)

    elif mode == 'args_get':
        return tuple(request.args.get(attr, dict_defo[attr]) for attr in attrs)


@app.route('/path_assessor_change', methods=['POST'])
def path_assessor_change():
    attrs = ['path_sub', 'assessor']
    path_sub, assessor = get_form_info(attrs)
    config2update = {'path_submission': path_sub, 'assessor': assessor}
    write_config(**config2update)
    return redirect(url_for('mc_editing'))


"""
Marking Criteria Editing Page (mc_editing)
"""


@app.route('/')
def mc_editing():
    config = read_config()
    path_sub, assessor = config['path_submission'], config['assessor']
    # GET only
    attrs = ['hw', 'cps_idx', 'cps_txt', 'cps_mark', 'gpp_idx', 'gpp_txt', 'gpp_mark', 'message']
    hw, cps_idx, cps_txt, cps_mark, gpp_idx, gpp_txt, gpp_mark, message = get_form_info(attrs, 'args_get')
    return render_template(
        'mc_editing.html',
        hw=hw,
        cps_idx=cps_idx,
        cps_txt=cps_txt,
        cps_mark=cps_mark,
        gpp_idx=gpp_idx,
        gpp_txt=gpp_txt,
        gpp_mark=gpp_mark,
        message=message,
        df_cps=mc.df_cps.to_html(na_rep='', border=2),
        df_gpp=mc.df_gpp.to_html(na_rep='', border=2),
        path_sub=path_sub,
        assessor=assessor,
    )


@ app.route('/add_cols', methods=['POST'])
def add_cols():
    hw, = get_form_info(['hw'])
    mc.df_add_cols(f'HW{hw}')
    return redirect(url_for('mc_editing', hw=hw))


@ app.route('/del_cols', methods=['POST'])
def del_cols():
    hw, = get_form_info(['hw'])
    mc.df_del_cols(f'HW{hw}')
    return redirect(url_for('mc_editing', hw=hw))


@ app.route('/cps_add', methods=['POST'])
def cps_add():
    attrs = ['hw', 'cps_idx', 'cps_txt', 'cps_mark']
    hw, cps_idx, cps_txt, cps_mark = get_form_info(attrs)
    df_cps = mc.df_cps
    df_cps.at[int(cps_idx), f'HW{hw}'] = f'{cps_txt} [{cps_mark}]'
    mc.df_cps = df_cps
    return redirect(url_for('mc_editing', hw=hw, cps_idx=cps_idx, cps_txt=cps_txt, cps_mark=cps_mark))


@ app.route('/cps_del', methods=['POST'])
def cps_del():
    attrs = ['hw', 'cps_idx']
    hw, cps_idx = get_form_info(attrs)
    df_cps = mc.df_cps
    df_cps.at[int(cps_idx), f'HW{hw}'] = np.nan
    mc.df_cps = df_cps
    return redirect(url_for('mc_editing', hw=hw, cps_idx=cps_idx))


@ app.route('/gpp_add', methods=['POST'])
def gpp_add():
    attrs = ['hw', 'gpp_idx', 'gpp_txt', 'gpp_mark']
    hw, gpp_idx, gpp_txt, gpp_mark = get_form_info(attrs)
    df_gpp = mc.df_gpp
    df_gpp.at[int(gpp_idx), f'HW{hw}'] = f'{gpp_txt} [{gpp_mark}]'
    mc.df_gpp = df_gpp
    return redirect(url_for('mc_editing', hw=hw, gpp_idx=gpp_idx, gpp_txt=gpp_txt, gpp_mark=gpp_mark))


@ app.route('/gpp_del', methods=['POST'])
def gpp_del():
    attrs = ['hw', 'gpp_idx']
    hw, gpp_idx = get_form_info(attrs)
    df_gpp = mc.df_gpp
    df_gpp.at[int(gpp_idx), f'HW{hw}'] = np.nan
    mc.df_gpp = df_gpp
    return redirect(url_for('mc_editing', hw=hw, gpp_idx=gpp_idx))


@ app.route('/save', methods=['POST'])
def save():
    path_sub = read_config()['path_submission']
    save_csv(mc.df_cps, mc.df_gpp, path_sub)
    load_mc()
    message = 'Marking Criteria has been saved!'
    return redirect(url_for('mc_editing', message=message))


@ app.route('/reload', methods=['POST'])
def reload():
    load_mc()
    message = 'Marking Criteria has been reloaded from local csv file.'
    return redirect(url_for('mc_editing', message=message))


"""
Marksheet page
"""


@app.route('/marking')
def marking():
    config = read_config()
    path_sub, assessor, template_common = config['path_submission'], config['assessor'], config['template_common_mistake']
    # GET only
    attrs = ['hw', 'sub_ids_str', 'sub_id_selected', 'points_str', 'point_selected', 'message', 'feedback', 'feedback_collection']
    hw, sub_ids_str, sub_id_selected, points_str, point_selected, message, feedback, feedback_collection = get_form_info(attrs, 'args_get')
    # Convert strings into lists
    lis_sub_ids = string2list(sub_ids_str)
    lis_points = string2list(points_str)
    lis_feedbacks = string2list(feedback_collection)
    # Marksheet
    sub_ids_with_selection = [{'value': id, 'selected': id == sub_id_selected} for id in lis_sub_ids]
    points_with_selection = [{'value': point, 'selected': point == point_selected} for point in lis_points]
    # Replace the splitter (///) by '\n\n'
    if feedback != '':
        feedback = feedback.replace('///', '\n\n')
    return render_template(
        'marking.html',
        hw=hw,
        sub_ids=sub_ids_with_selection,
        sub_id_selected=sub_id_selected,
        points=points_with_selection,
        point_selected=point_selected,
        df_ms=df_scrollable(ms.df_ms),
        message=message,
        feedback=feedback,
        feedback_collection=lis_feedbacks,
        template_common=template_common,
        path_sub=path_sub,
        assessor=assessor,
    )


@ app.route('/confirm_setups', methods=['POST'])
def confirm_setups():
    load_mc()
    config = read_config()
    path_sub, template_common = config['path_submission'], config['template_common_mistake']
    attrs = ['hw', 'sub_id_selected', 'feedback_collection']
    hw, sub_id_selected, feedback_collection = get_form_info(attrs, feedback_collection=['feedback 1', 'feedback 2'])

    path_full = os.path.join(path_sub, f'HW{hw}')
    ms.path_marksheet = os.path.join(path_sub, f'HW{hw}_marksheet.csv')
    try:
        message = path_full
        sub_ids = get_folders(path_full)
    except FileNotFoundError:
        sub_ids = ['submission 1', 'submission 2', 'submission 3', 'etc.']
        message = '!! FileNotFound !!'
    # Load the marksheet for the particular homework (identified by 'term' and 'hw')
    ms.get_marksheet(hw, sub_ids)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    feedback_collection_str = list2string(feedback_collection)
    return redirect(url_for(
        'marking',
        hw=hw,
        sub_ids_str=sub_ids_str,
        points_str=points_str,
        sub_id_selected=sub_id_selected,
        message=message,
        feedback_collection=feedback_collection_str,
        template_common=template_common,
    ))


@ app.route('/give_mark', methods=['POST'])
def give_mark():
    path_sub = read_config()['path_submission']
    attrs = ['hw', 'sub_id_selected', 'point_selected', 'mark_int', 'mark_dec']
    hw, sub_id_selected, point_selected, mark_int, mark_dec = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    sub_ids = get_folders(path_full)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    # Check if the mark awarded is not exceeding the full mark
    mark = float(mark_int) + float(mark_dec) * 0.1
    _, fullmark = get_marks(point_selected)
    if mark > float(fullmark):
        mark = np.nan
    ms.df_ms.at[sub_id_selected, point_selected] = mark

    #  --------- !!!! Should not the marksheet be saved to csv everytime when a mark is added ?????? !!!! --------------------------
    # Make a function to load all the user input info on the form

    return redirect(url_for(
        'marking',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        points_str=points_str,
        point_selected=point_selected
    ))


@ app.route('/save_marksheet', methods=['POST'])
def save_marksheet():
    #  --------- !!!! Is this necessary??? !!!! --------------------------
    path_sub = read_config()['path_submission']
    attrs = ['hw', 'sub_id_selected', 'point_selected']
    hw, sub_id_selected, point_selected = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    sub_ids = get_folders(path_full)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    save_csv(ms.df_ms, ms.path_marksheet)
    message = f'Marksheet has been saved to: {ms.path_marksheet}'
    return redirect(url_for(
        'marking',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        points_str=points_str,
        point_selected=point_selected,
        message=message,
    ))


@ app.route('/load_feedback', methods=['POST'])
def load_feedback():
    path_sub = read_config()['path_submission']
    attrs = ['hw', 'sub_id_selected', 'point_selected', 'feedback']
    hw, sub_id_selected, point_selected, feedback = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    sub_ids = get_folders(path_full)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    # Load feedbacks for the selected submission
    feedback = ms.df_ms.loc[sub_id_selected, 'Feedback']
    message = f'Load: Feedback for submission by {sub_id_selected} for homework HW{hw}'
    return redirect(url_for(
        'marking',
        hw=hw,
        message=message,
        feedback=feedback,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        points_str=points_str,
        point_selected=point_selected
    ))


@ app.route('/add_feedback', methods=['POST'])
def add_feedback():
    path_sub = read_config()['path_submission']
    attrs = ['hw', 'sub_id_selected', 'point_selected', 'feedback']
    hw, sub_id_selected, point_selected, feedback = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    sub_ids = get_folders(path_full)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    # Edit feedbacks for the selected submission
    # if feedback != '':
    # --------- !!!! make a func that simply save the feedback to be used in other function, too !!!! --------------------------
    feedback = re.sub(r'(\r\n|\r|\n){2}', '///', feedback)
    # Trim unnecessary strings
    if feedback.endswith(' '):
        feedback = feedback[:-1]
    if feedback.endswith('///'):
        feedback = feedback[:-3]
    ms.df_ms.at[sub_id_selected, 'Feedback'] = feedback
    message = f'Saved: Feedback for submission by {sub_id_selected} for homework HW{hw}'
    return redirect(url_for(
        'marking',
        hw=hw,
        message=message,
        feedback=feedback,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        points_str=points_str,
        point_selected=point_selected
    ))


@ app.route('/save_common_mistakes', methods=['POST'])
def save_common_mistakes():
    path_sub = read_config()['path_submission']
    attrs = ['hw', 'sub_id_selected', 'point_selected', 'feedback', 'template_common']
    hw, sub_id_selected, point_selected, feedback, template_common = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    sub_ids = get_folders(path_full)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    write_config(**{'template_common_mistake': template_common})
    message = f'Saved: Common Mistakes for homework HW{hw}'

    # --------- !!!! Should or should not save the mark and feedback at the same time ?????? !!!! --------------------------

    return redirect(url_for(
        'marking',
        hw=hw,
        message=message,
        feedback=feedback,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        points_str=points_str,
        point_selected=point_selected,
        template_common=template_common
    ))

# Feedback collection bottuns, implement


"""
Report Generation Page
"""


@app.route('/reporting')
def reporting():
    config = read_config()
    path_sub, assessor, col_styles = config['path_submission'], config['assessor'], config['col_styles']
    # GET only
    attrs = ['hw', 'sub_ids_str', 'sub_id_selected', 'message', 'summary', 'template_head', 'template_common', 'cmode_selected']
    hw, sub_ids_str, sub_id_selected, message, summary, template_head, template_common, cmode_selected = get_form_info(attrs, 'args_get')
    # Convert strings into lists
    lis_sub_ids = string2list(sub_ids_str)
    # Marksheet
    sub_ids_with_selection = [{'value': id, 'selected': id == sub_id_selected} for id in lis_sub_ids]
    cmodes_with_selection = [{'example': cstyle, 'id': f'cmode{col_styles.index(cstyle)}', 'selected': str(col_styles.index(cstyle)) == cmode_selected[5:]} for cstyle in col_styles]
    summary_html = markdown.markdown(summary, extensions=['tables'])

    return render_template(
        'reporting.html',
        hw=hw,
        sub_ids=sub_ids_with_selection,
        sub_id_selected=sub_id_selected,
        df_ms=df_scrollable(ms.df_ms),
        message=message,
        template_head=template_head,
        template_common=template_common,
        summary=summary,
        summary_html=summary_html,
        path_sub=path_sub,
        assessor=assessor,
        cmode_selected=cmode_selected,
        cmodes_with_selection=cmodes_with_selection,
    )


@ app.route('/confirm_homework', methods=['POST'])
def confirm_homework():
    path_sub = read_config()['path_submission']
    load_mc()
    attrs = ['hw', 'sub_id_selected', 'cmode_selected']
    hw, sub_id_selected, cmode_selected = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    ms.path_marksheet = os.path.join(path_sub, f'HW{hw}_marksheet.csv')
    try:
        message = path_full
        sub_ids = get_folders(path_full)
    except FileNotFoundError:
        sub_ids = ['submission 1', 'submission 2', 'submission 3', 'etc.']
        message = '!! FileNotFound !!'
    # Load the marksheet for the particular homework (identified by 'term' and 'hw')
    ms.get_marksheet(hw, sub_ids)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    return redirect(url_for(
        'reporting',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        message=message,
        cmode_selected=cmode_selected,
    ))


@ app.route('/confirm_sub_id', methods=['POST'])
def confirm_sub_id():
    load_mc()
    path_sub = read_config()['path_submission']
    attrs = ['hw', 'sub_id_selected', 'template_head', 'template_common', 'cmode_selected']
    hw, sub_id_selected, template_head, template_common, cmode_selected = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    ms.path_marksheet = os.path.join(path_sub, f'HW{hw}_marksheet.csv')
    try:
        message = path_full
        sub_ids = get_folders(path_full)
    except FileNotFoundError:
        sub_ids = ['submission 1', 'submission 2', 'submission 3', 'etc.']
        message = '!! FileNotFound !!'
    # Load the marksheet for the particular homework (identified by 'term' and 'hw')
    ms.get_marksheet(hw, sub_ids)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    return redirect(url_for(
        'reporting',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        message=message,
        template_head=template_head,
        template_common=template_common,
        cmode_selected=cmode_selected,
    ))


@app.route('/update_template_head', methods=['POST'])
def update_template_head():
    attrs = ['hw', 'sub_id_selected', 'template_head', 'cmode_selected']
    hw, sub_id_selected, template_head, cmode_selected = get_form_info(attrs)

    path_sub = read_config()['path_submission']
    path_full = os.path.join(path_sub, f'HW{hw}')
    ms.path_marksheet = os.path.join(path_sub, f'HW{hw}_marksheet.csv')
    try:
        message = path_full
        sub_ids = get_folders(path_full)
    except FileNotFoundError:
        sub_ids = ['submission 1', 'submission 2', 'submission 3', 'etc.']
        message = '!! FileNotFound !!'
    # Load the marksheet for the particular homework (identified by 'term' and 'hw')
    ms.get_marksheet(hw, sub_ids)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    write_config(**{'template_head': template_head})

    return redirect(url_for(
        'reporting',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        message=message,
        template_head=template_head,
        cmode_selected=cmode_selected,
    ))


@app.route('/generate', methods=['POST'])
def generate():
    load_mc()
    config = read_config()
    path_sub, assessor, template_common = config['path_submission'], config['assessor'], config['template_common_mistake']

    attrs = ['hw', 'sub_id_selected', 'template_head', 'cmode_selected']
    hw, sub_id_selected, template_head, cmode_selected = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    ms.path_marksheet = os.path.join(path_sub, f'HW{hw}_marksheet.csv')
    try:
        message = path_full
        sub_ids = get_folders(path_full)
    except FileNotFoundError:
        sub_ids = ['submission 1', 'submission 2', 'submission 3', 'etc.']
        message = '!! FileNotFound !!'
    # Load the marksheet for the particular homework (identified by 'term' and 'hw')
    ms.get_marksheet(hw, sub_ids)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    summary = generate_summary(sub_id_selected, ms.df_ms, hw, mc, assessor, template_head, template_common, cmode_selected[5:])

    return redirect(url_for(
        'reporting',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        message=message,
        template_head=template_head,
        template_common=template_common,
        summary=summary,
        cmode_selected=cmode_selected,
    ))


@app.route('/ipynb2pdf', methods=['POST'])
def ipynb2pdf_all():
    """
    Use multiprocessing to convert ipynb to pdf. cnvrt_win.cmd is called in each subprocess.
    Want to show real time log on the screen using socketIO.
    So far, just disable all the buttons while executing the command. If error, recommend to brows back.
    """
    attrs = ['hw', 'sub_id_selected', 'template_head', 'cmode_selected']
    hw, sub_id_selected, template_head, cmode_selected = get_form_info(attrs)

    path_full = os.path.join(path_sub, f'HW{hw}')
    ms.path_marksheet = os.path.join(path_sub, f'HW{hw}_marksheet.csv')
    try:
        sub_ids = get_folders(path_full)
    except FileNotFoundError:
        sub_ids = ['submission 1', 'submission 2', 'submission 3', 'etc.']
    # Load the marksheet for the particular homework (identified by 'term' and 'hw')
    ms.get_marksheet(hw, sub_ids)
    sub_ids_str, points_str = list2string_routine(sub_ids, ms)

    # Converting the files. Somehow need to output messages...
    ipynb2pdf(hw, multiprocess=True)
    """
    multiprocessing, pool size 3, run: 91, 75 s
    multiprocessing, pool size 16, run: 40 s
    multiprocessing, pool size 3, Popen: error
    subprocess, run: 180 s
    subprocess, Popen: error
    """

    return redirect(url_for(
        'reporting',
        hw=hw,
        sub_ids_str=sub_ids_str,
        sub_id_selected=sub_id_selected,
        message='.ipynb files have been  converted to .pdf',
        template_head=template_head,
        template_common=template_common,
        summary='',
        cmode_selected=cmode_selected,
    ))


def ipynb2pdf(hw, **kwargs):
    """
    Convert ALL the .ipynb files into .pdf files. If multiprocessing, creaste queue, and start the processes.
    Parameters:
        mprocerss: True by default. If use multiprocessing or not.
        poolsize: cpu_count by default. Pool size for the multiprocessing.
    """
    mprocess = kwargs.pop('multiprocess', True)
    poolsize = kwargs.pop('poolsize', cpu_count())
    print('CPU count: ', poolsize)
    print('!!!!!!!!!!!!!!!!!!!!!START!!!!!!!!!!!!!!!!!!!!!!!!')
    ts = time.time()
    config = read_config()
    condaenv = config['condaenv']
    path_hw = os.path.join(config['path_submission'], f'HW{hw}')
    lis_direc = os.listdir(path_hw)

    if mprocess:
        manager = Manager()
        queue_log = manager.Queue()
        queue_work = Queue()

    # For each submission id, loop & visualise the progress.
    for f in lis_direc:
        # If there is a .ipnb file, convert that to .pdf
        path_ff = os.path.join(path_hw, f, 'File submissions')
        for ff in os.listdir(path_ff):
            if ff.endswith('.ipynb'):
                # Run the command to convert ipynb to pdf
                if mprocess:
                    queue_work.put((condaenv, ff, path_ff, queue_log))
                else:
                    subprocess.Popen(f'cvrt_win.cmd {condaenv} {ff} "{path_ff}"')
    if mprocess:
        # logging.debug('Start')
        processes = [Process(target=ipy2pdf_worker, args=(queue_work, queue_log)) for _ in range(poolsize)]
        processes.append(Process(target=log_worker, args=(queue_log,)))
        for process in processes:
            process.start()

        for process in processes:
            process.join()
        # logging.debug('End')
    te = time.time()
    print('!!!!!!!!!!!!!!!!!!!!!END!!!!!!!!!!!!!!!!!!!!!!!!')
    print(te - ts)


def ipy2pdf_worker(queue_work, queue_log):
    """
    Subprocess for ipynb2pdf().
    Refereced...:
        https://qiita.com/COJICOJI/items/d402f9ba5ad715fa4c23
        https://tech.nkhn37.net/python-multiprocessing-basics/#Queue
        https://shun-studio.com/python/multiprocess-single-log/
    """
    # Repeat while the queue is not empty
    while not queue_work.empty():
        try:
            condaenv, ff, path_ff, queue_log = queue_work.get_nowait()
        except Empty:
            break
        else:
            try:
                subprocess.run(f'cvrt_win.cmd {condaenv} {ff} "{path_ff}"')
                queue_log.put(f'cvrt_win.cmd {condaenv} {ff} "{path_ff}"')
            except subprocess.CalledProcessError as e:
                print(e)
                queue_log.put(e)


def log_worker(queue_log):
    while not queue_log.empty():
        try:
            msg = queue_log.get()
        except Empty:
            break
        else:
            print('<' * 100)
            print("[LOG]:", msg)
            print('>' * 100)


if __name__ == ('__main__'):
    import eventlet
    load_mc()
    # app.run(debug=True, host='0.0.0.0', port=5050)
    eventlet.monkey_patch()
    # socketio.run(app, host='0.0.0.0', port=5000, debug=True)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=False)
