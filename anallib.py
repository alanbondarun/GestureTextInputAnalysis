import re
import statistics

res_directory = "res"
file_ext = ".csv"

task_ww_filename = "TaskRecordGlassWatchWriteActivity"
task_1d_filename = "TaskRecordGlassOneDActivity"

def parse_csv(filepath, header = False):
    file = filepath.open()
    line_list = []
    linenum = 0
    for line in file:
        if (linenum == 0 and header) or linenum > 2:
            values = line.strip().split("\"")
            value_list = []
            in_str = False
            for value_str in values:
                if in_str:
                    value_list.append(value_str)
                else:
                    for item in value_str.split(","):
                        if item != '':
                            value_list.append(item)
                in_str = not in_str

            line_list.append(value_list)
        linenum += 1
    return line_list

def parse_timed_actions(csv_list):
    for csv_line in csv_list:
        timed_actions = []
        timed_actions_str = csv_line.pop()
        for timed_action_str in re.findall('\[[^\]]*\]', timed_actions_str):
            timed_actions.append(timed_action_str.strip("[]").split(","))
        csv_line.append(timed_actions)
    return csv_list

def extract_timed_actions(parsed_values):
    timed_actions = []
    for expr_unit in parsed_values:
        for list_line in expr_unit:
            timed_actions.append(list_line[-1])
    return timed_actions

def calculate_keypress_time(timed_actions):
    keys = []
    keypress_times = []
    for timed_action in timed_actions:
        for i in range(len(timed_action)-1):
            cinterval = float(timed_action[i+1][0]) - float(timed_action[i][0])
            if not (timed_action[i+1][1] in keys):
                keys.append(timed_action[i+1][1])
                keypress_times.append([cinterval])
            else:
                key_idx = keys.index(timed_action[i+1][1])
                keypress_times[key_idx].append(cinterval)

    result = []
    for i in range(len(keys)):
        values = [keys[i], sum(keypress_times[i]) / len(keypress_times[i]), len(keypress_times[i])]
        if (len(keypress_times[i]) >= 2):
            values.append(statistics.stdev(keypress_times[i]))
        else:
            values.append(0)
        result.append(values)
    return result