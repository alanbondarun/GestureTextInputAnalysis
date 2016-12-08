import re
import statistics

res_directory = "res"
file_ext = ".csv"

task_ww_filename = "TaskRecordGlassWatchWriteActivity"
task_1d_filename = "TaskRecordGlassOneDActivity"

def parse_csv(filepath, header = False, start_from = 1):
    file = filepath.open()
    line_list = []
    linenum = 0
    for line in file:
        if (linenum == 0 and header) or linenum >= start_from:
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

    file.close()
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

def get_uncorrected_errors(expected_str, input_str):
    nums = [[0 for x in range(len(input_str) + 1)] for y in range(len(expected_str) + 1)]
    commands = [[0 for x in range(len(input_str) + 1)] for y in range(len(expected_str) + 1)]
    cmd_insert = 1
    cmd_delete = 2
    cmd_correct = 3
    cmd_modify = 0

    for i in range(1, len(expected_str) + 1):
        nums[i][0] = i
        commands[i][0] = cmd_insert
    for j in range(1, len(input_str) + 1):
        nums[0][j] = j
        commands[0][j] = cmd_delete
    for i in range(1, len(expected_str) + 1):
        for j in range(1, len(input_str) + 1):
            if expected_str[i-1] == input_str[j-1]:
                nums[i][j] = nums[i-1][j-1]
                commands[i][j] = cmd_correct
            else:
                minval = min(nums[i-1][j], nums[i][j-1], nums[i-1][j-1])
                if minval == nums[i-1][j]:
                    nums[i][j] = nums[i-1][j] + 1
                    commands[i][j] = cmd_insert
                elif minval == nums[i][j-1]:
                    nums[i][j] = nums[i][j-1] + 1
                    commands[i][j] = cmd_delete
                else:
                    nums[i][j] = nums[i-1][j-1] + 1
                    commands[i][j] = cmd_modify

    pos_i = len(expected_str)
    pos_j = len(input_str)
    dict_error = {}
    while pos_i > 0 and pos_j > 0:
        if commands[pos_i][pos_j] == cmd_correct:
            pos_i -= 1
            pos_j -= 1
        elif commands[pos_i][pos_j] == cmd_insert:
            pos_i -= 1
        elif commands[pos_i][pos_j] == cmd_delete:
            pos_j -= 1
            if input_str[pos_j] not in dict_error:
                dict_error[input_str[pos_j]] = 1
            else:
                dict_error[input_str[pos_j]] += 1
        else:
            pos_i -= 1
            pos_j -= 1
            if input_str[pos_j] not in dict_error:
                dict_error[input_str[pos_j]] = 1
            else:
                dict_error[input_str[pos_j]] += 1
    while pos_j > 0:
        pos_j -= 1
        if input_str[pos_j] not in dict_error:
            dict_error[input_str[pos_j]] = 1
        else:
            dict_error[input_str[pos_j]] += 1

    return dict_error

# dictionary of [num-keys, num-corrected-errors, num-uncorrected-errors]
def aggregate_errors(keypress_files):
    keys = {}
    for keypress_file in keypress_files:
        for keypress_sentence in keypress_file:
            timed_actions = keypress_sentence[-1]
            input_str = ""
            for i in range(len(timed_actions)):
                if timed_actions[i][1] == 'cancel':
                    continue
                if timed_actions[i][1] == 'del':
                    if len(input_str) > 0:
                        keys[input_str[-1]][1] += 1
                        input_str = input_str[:-1]
                elif timed_actions[i][1] not in keys:
                    keys[timed_actions[i][1]] = [1, 0, 0]
                    input_str += timed_actions[i][1]
                else:
                    keys[timed_actions[i][1]][0] += 1
                    input_str += timed_actions[i][1]

            uncorrect_dict = get_uncorrected_errors(keypress_sentence[-3], keypress_sentence[-2])
            for key in uncorrect_dict:
                keys[key][2] += 1

    return keys
