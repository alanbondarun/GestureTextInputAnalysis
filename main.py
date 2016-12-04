from pathlib import Path
import re

res_directory = "res"
task_ww_filename = "TaskRecordGlassWatchWriteActivity"
task_1d_filename = "TaskRecordGlassOneDActivity"
file_ext = ".csv"

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

            timed_actions = []
            timed_actions_str = value_list.pop()
            for timed_action_str in re.findall('\[[^\]]*\]', timed_actions_str):
                timed_actions.append(timed_action_str.strip("[]").split(","))
            value_list.append(timed_actions)

            line_list.append(value_list)
        linenum += 1
    return line_list

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
        result.append([keys[i], sum(keypress_times[i]) / len(keypress_times[i])])
    return result

file_list = [x for x in Path(res_directory).iterdir() if x.is_file()]

ww_parsed_values = []
oned_parsed_values = []

for file in file_list:
    if str(file).endswith(task_ww_filename + file_ext):
        ww_parsed_values.append(parse_csv(file))
    elif str(file).endswith(task_1d_filename + file_ext):
        oned_parsed_values.append(parse_csv(file))

ww_timed_actions = extract_timed_actions(ww_parsed_values)
oned_timed_actions = extract_timed_actions(oned_parsed_values)

ww_keypress_times = calculate_keypress_time(ww_timed_actions)
ww_keypress_times.sort()

oned_keypress_times = calculate_keypress_time(oned_timed_actions)
oned_keypress_times.sort()

print([item[1] for item in ww_keypress_times])
print([item[1] for item in oned_keypress_times])