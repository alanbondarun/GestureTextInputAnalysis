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


file_list = [x for x in Path(res_directory).iterdir() if x.is_file()]

ww_parsed_values = []
oned_parsed_values = []

for file in file_list:
    if str(file).endswith(task_ww_filename + file_ext):
        ww_parsed_values.append(parse_csv(file))
    elif str(file).endswith(task_1d_filename + file_ext):
        oned_parsed_values.append(parse_csv(file))
