# nback
Verbal version of the nback task coded in python for MR scanner use as a working-memory paradigm. Variables and stimuli are determined from an input csv (not hard-coded) so the task is easy to edit for personal use. Requires PsychoPy.

Task Parameters
---------------
0-, 1-, and 2-back conditions.
Instruction slide on the screen for 3000ms at the beginning of each block.
Letter stimuli on the screen for 500ms, followed by 2500ms fixation, followed by jittered fixation (15, 17, or 19s) at the end of the block.
2 runs - 9 blocks each (3 for each condition) - 10 trials in each block.
14 min total (7min for each run).

Stimuli are loaded into a local dictionary before the task begins so as not to affect the task timing during the actual trials.

Runs
----
The pop-up window asks for run type: scanner, backup, or practice.
- Scanner runs the entire tasks - both runs with a pause in between to check in with subject. This uses nback_AB.csv.
- Backup runs just the second run of the task - use this if PsychoPy crashes during the task and you only need to run the second half. This uses nback_B.csv
- Practice runs a mini-version of the task that can be administered to participants before beginning the full task. There is one block each of the 0-, 1-, and 2-back conditions. This uses nback_practice.csv.

Subject key responses
--------------------
Keys pressed can be edited in the code itself. Current target keys are 1 (right-handed index finger button box press) and 4 (left-handed index finger button box press). Space bar moves through the instructions and + moves through the trigger slide (space bar will also move past this slide for ease of testing/starting task outside of scanner).

Output
------
The task outputs a csv containing statistics for: 
- **Total correct hits** - target letter was correctly identified.
- **Total correct skips** - non-target letter was correctly skipped.
- **Total false alarms** - subject pressed key on a non-target letter.
- **Total misses** - target letter was not identified.
- **Overall accuracy** - percent of correct hits and skips.
- **Hit accuracy** - percent of correct hits.
- **False alarm rate** - percent of false alarms out of total non-target letters.
- **Average reaction time** - average time for participant pressing button after initial onset of the stimuli.
