"""Task documentation"""

from __future__ import absolute_import, division, print_function
from psychopy import core, data, event, gui, logging, visual
import numpy as np
import os
import sys
import time
import pandas as pd

# change directory to current directory
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# store info about the experiment session
expName = 'Nback'
expInfo = {'participant' : '',
            'run' : ['Scanner', 'Practice', 'Backup']}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if not dlg.OK:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['participant'] = str(expInfo['participant'])

# create filename with relevant info
if expInfo['run'] == 'Scanner':
    filename = os.path.join(_thisDir, 'tfMRI_output',
        '%s_%s_%s'%(expInfo['participant'],expInfo['expName'],expInfo['date']))
elif expInfo['run'] == 'Practice':
    filename = os.path.join('/Users', 'gablab', 'Desktop', 'Practice',
        '%s_%s_%s'%(expInfo['participant'],expInfo['expName'],expInfo['date']))
else:
    filename = os.path.join(_thisDir, 'tfMRI_output', 'backup',
        '%s_%s_%s'%(expInfo['participant'],expInfo['expName'],expInfo['date']))

outfile = "{}.csv".format(filename)

# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # This outputs to the screen

# csv to be read
if expInfo['run'] == 'Scanner':
    filepaths = "nback_AB.csv"
    df_trials_AB = pd.read_csv(filepaths, index_col=False)
elif expInfo['run'] == 'Practice':
    filepaths = "nback_practice.csv"
    df_trials_practice = pd.read_csv(filepaths, index_col=False)
else:
    filepaths = "nback_B.csv"
    df_trials_backup = pd.read_csv(filepaths, index_col=False)

# create window - black screen
win = visual.Window(
    fullscr=True, screen=0, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[-1,-1,-1], colorSpace='rgb',
    blendMode='avg', useFBO=True)

# set up text objects
instructions_text = visual.TextStim(win,
    text='For this game you will remember which letters were presented 0, 1, \
or 2 trials ago, and report when the current letters are repeats. \
Press the button under your index finger for repeated letters.',
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

experimenter_text = visual.TextStim(win,text="Waiting for the experimenter.",
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

trigger_text = visual.TextStim(win, text="Waiting for the scanner.",
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

thanks_text = visual.TextStim(win, text='Thanks!',
    pos=(0,0), colorSpace='rgb', color=1, height=0.1, wrapWidth=1.5, depth=0.0)

def save_on_quit(df):
    """ If escape key is pressed, quit task and save data collected to csv.
    df : main dataframe that data is saved to """
    if event.getKeys(keyList=["escape"]):
        win.close()
        core.quit()

    df.to_csv(outfile, index=True)

def hit_or_miss(df, corr_right, corr_left, trun, rt, key_pressed,
                key_pressed_first, total_correct_hits, total_correct_skips,
                total_false_alarm, total_misses, rxn_time_sum, not_0):
    """ Collects stats and calculates accuracy, hit accuracy, false alarm rate,
        and average reaction times for each iteration. Saves info to df_master
        and returns "total" stats.

    Parameters
    ----------
    df : pd.DataFrame
    corr_right : float of correct key presses for right hand
    corr_left : float of correct key presses for left hand
    trun : block clock
    rt : float of reaction time
    key_pressed : list of keypresses and reaction times
    key_pressed_first : int of just the first key pressed (unless nan)
    total_correct_hits : int number of correct answers
    total_correct_skips : int number of correct skips
    total_false_alarm : int number of hits when correct answer is 0
    total_misses : int number skipped
    rxn_time_sum : float sum of reaction times for each iteration (trial)
    not_0 : int number of total answered iterations (trials)

    Local Variables
    ---------------
    num_correct_hits : int number of correct answers
    num_correct_skips : int number of correct skips
    num_false_alarm : int number of hits when correct answer is 0
    num_misses : int number skipped
    """
    # start counters at 0 for each trial
    num_correct_hits = 0
    num_correct_skips = 0
    num_false_alarm = 0
    num_misses = 0

    # collect stats based on key press and reaction time
    if rt is not None:
        rxn_time_sum += rt
        not_0 += 1

    # to avoid collecting stats from instructions row (i.e. "0-back instr")
    if pd.isnull(corr_left):
        num_misses = 0
        num_correct_skips = 0

    # if the letter isn't correct and the subject correctly skips it
    elif key_pressed_first is None and corr_left == 0:
        num_correct_skips += 1
        total_correct_skips += 1

    # if the letter isn't correct and the subject incorrectly presses a key
    elif key_pressed_first and corr_left == 0:
        num_false_alarm += 1
        total_false_alarm += 1

    # if the letter is correct and the subject correctly hits a key.
    elif key_pressed_first in [corr_left, corr_right] and corr_left != 0:
        num_correct_hits += 1
        total_correct_hits += 1

    # if the letter is correct and the subject doesn't press a key.
    else:
        num_misses += 1
        total_misses += 1

    # calculate accuracy, hit accuracy, false alarm rate and avg reaction time
    total_sum = (total_correct_hits
                 + total_correct_skips
                 + total_misses
                 + total_false_alarm)

    total_pos = (total_correct_hits
                + total_misses)

    total_neg = (total_false_alarm
                + total_correct_skips)

    if total_sum == 0:
        overall_accuracy = None
    else:
        overall_accuracy = (((total_correct_hits
                            + total_correct_skips)
                            *100.0)/total_sum)

    if total_pos == 0:
        hit_accuracy = None
    else:
        hit_accuracy = (total_correct_hits*100.0)/total_pos

    if total_neg == 0:
        false_alarm_rate = None
    else:
        false_alarm_rate = (total_false_alarm*100.0)/total_neg

    if not_0 == 0:
        avg_rxn_time = None
    else:
        avg_rxn_time = (rxn_time_sum/not_0)

    # output stats to dataframe
    df.loc[len(df), :] = [key_pressed, key_pressed_first, rt, corr_right,
                        corr_left, trun, num_correct_hits, num_correct_skips,
                        num_false_alarm, num_misses, total_correct_hits,
                        total_correct_skips, total_false_alarm, total_misses,
                        overall_accuracy, hit_accuracy, false_alarm_rate,
                        avg_rxn_time]

    # return variables that don't reset each trial (summary stats)
    return (total_correct_hits, total_correct_skips, total_false_alarm,
    total_misses, rxn_time_sum, not_0, overall_accuracy, hit_accuracy,
    false_alarm_rate, avg_rxn_time)

def retrieve_key_response(df, time):
    """ Get keys pressed and reaction times. Returns local variables.

    Parameters
    ----------
    df : pd.DataFrame
    time : clock time to record key press reaction time

    Local Variables
    ---------------
    key_pressed : list of recorded keys pressed by subject
    key_pressed_first : int of first key pressed by the subject
    rt : float reaction time from keyPressed
    """
    key_pressed = event.getKeys(keyList=['1', '4'], timeStamped=time)
    if not key_pressed:
        key_pressed = key_pressed_first = rt = None
        return key_pressed, key_pressed_first, rt
    else:
        key_pressed_first = key_pressed[0][0]
        rt = key_pressed[0][1]  # get first reaction time
        return key_pressed, int(key_pressed_first), rt

def get_image_stim_mapping(list_of_filepaths, win=win):
    """Return dictionary of image objects given pd.Series object of filepaths.
    """
    list_of_filepaths = list_of_filepaths.unique()
    return {fp: visual.ImageStim(win=win, image=fp) for fp in list_of_filepaths}

def trials(run_trial):
    """ Main function calls all the other functions to collect data, stats, and
        display images. Saves "summary" stats to df_totals and saves both
        DataFrames as csv files.

    Parameters
    ----------
    run_trial : determines if we run A or B

    Local Variables
    ---------------
    clock : clock to record time
    block_clock : clock to record the start of new blocks (running time)
    header_cols : list of names of data frame columns for df_master
    df_master : empty data frame to add collected data to
    column_names : list of names of data frame columns for df_totals
    df_totals : empty data frame to add summary of stats to
    total_correct_hits : int running total number of hits on correct letters
    total_correct_skips : int running total number of skips on incorrect letters
    total_false_alarm : int running total number of hits on incorrect letters
    total_misses : int running total number of skips on correct letters
    rxn_time_sum : float running total of all reaction times summed together
    not_0 : int running total of number of key presses
    stim_mapping : displays image from csv
    letter_fix_pairs : groups rows in csv by 2
    letter_image : shows image of letter in nback (or instructions)
    fix_image : shows image of fixation cross in nback
    correct_right : int of correct responses for right hand from csv
    correct_left : int of correct responses for left hand from csv
    letter_wait_time : time letter_image is displayed for
    fix_wait_time : time fix_image is displayed for
    block_time : int 1 if new block, 0 if not
    """
    clock = core.Clock()
    block_clock = core.Clock()

    # set up empty DataFrame to store experiment data
    header_cols = ['subj_key_resp', 'subj_key_resp_first', 'rxn_time',
                'corr_resp', 'corr_resp_left', 'running_time', 'hits',
                'corr_skips', 'false_alarm', 'misses', 'total_hits',
                'total_corr_skips', 'total_false_alarm', 'total_misses',
                'overall_accuracy', 'hit_accuracy', 'false_alarm_rate',
                'avg_rxn_time']
    df_master = pd.DataFrame(columns=header_cols)

    # set up empty data frame to collect total summary of stats
    column_names = ['total_hits', 'total_corr_skips', 'total_false_alarm',
                'total_misses', 'total_accuracy', 'hit_accuracy',
                'false_alarm_rate', 'avg_rxn_time']
    df_totals = pd.DataFrame(columns=column_names)

    # start summary counters at 0
    total_correct_hits = 0
    total_correct_skips = 0
    total_false_alarm = 0
    total_misses = 0
    rxn_time_sum = 0
    not_0 = 0

    # retrieve stimuli dictionary
    stim_mapping = get_image_stim_mapping(run_trial.loc[:, 'image_name'])

    # dataframe/csv read in pairs because ISI is included in its own row
    letter_fix_pairs = run_trial.groupby(run_trial.index.values // 2)

    # this loop runs the trials
    for idx, pair in letter_fix_pairs:
        # retrieve variables from csv
        idx *= 2
        letter_image = stim_mapping[pair.loc[idx, 'image_name']]
        fix_image = stim_mapping[pair.loc[idx+1, 'image_name']]
        correct_right = (pair.loc[idx, 'corr_resp'])
        correct_left = (pair.loc[idx, 'corr_resp_left'])
        letter_wait_time = float(pair.loc[idx, 'trial_dur'])
        fix_wait_time = float(pair.loc[idx+1, 'trial_dur'])
        block_time = int(pair.loc[idx, 'new_block'])

        # to pause halfway through in between A and B runs
        if expInfo['run'] == 'Scanner':
            run_type = str(pair.loc[idx, 'A_or_B'])
            if run_type == 'B':
                begin_slides()

        # record start time of each block
        if block_time == 1:
            run_time = block_clock.getTime()
        else:
            run_time = None

        # display stimulus
        t0 = time.time()
        clock.reset()
        while time.time() - t0 < letter_wait_time:
            letter_image.draw()
            win.flip()
            save_on_quit(df_master)

        # display fixation
        t0 = time.time()
        while time.time() - t0 < fix_wait_time:
            fix_image.draw()
            win.flip()
            save_on_quit(df_master)

        # call retrieve_key_response and save local variables
        key_pressed, key_pressed_first, rt = retrieve_key_response(df_master,
                                                                clock)

        # call stats function
        (total_correct_hits, total_correct_skips, total_false_alarm,
        total_misses, rxn_time_sum, not_0, overall_accuracy, hit_accuracy,
        false_alarm_rate, avg_rxn_time) = hit_or_miss(df_master, correct_right,
                                        correct_left, run_time, rt, key_pressed,
                                        key_pressed_first, total_correct_hits,
                                        total_correct_skips, total_false_alarm,
                                        total_misses, rxn_time_sum, not_0)

    # output stats to dataframe and then save to csv file
    df_totals.loc[len(df_totals), :] = [total_correct_hits, total_correct_skips,
                                    total_false_alarm, total_misses,
                                    overall_accuracy, hit_accuracy,
                                    false_alarm_rate, avg_rxn_time]
    df_totals.to_csv("{}_Summary.csv".format(filename), index=False)

    df_master.to_csv(outfile, index=True)

def print_instructions():
    """ Short function to display instructions slides """
    instructions_text.draw()
    win.flip()
    event.waitKeys(keyList=['1', '2', '3', '4', 'space'])

def begin_slides():
    """ Shortcut to display beginning slide and trigger """
    experimenter_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])

    trigger_text.draw()
    win.flip()
    event.waitKeys(keyList=['num_add', '+', 'space'])

# run experiment
if expInfo['run'] == 'Scanner':
    print_instructions()
    begin_slides()
    trials(df_trials_AB)
elif expInfo['run'] == 'Practice':
    print_instructions()
    trials(df_trials_practice)
else:
    begin_slides()
    trials(df_trials_backup)

logging.flush()

# Display end slide
thanks_text.draw()
win.flip()
event.waitKeys(keyList=['space'])

win.close()
core.quit()
