from pathlib import Path
from anallib import *
from motionlib import *

file_list = [x for x in Path(res_directory).iterdir() if x.is_file()]

ww_parsed_values = []
oned_parsed_values = []
ww_motion_values = []
oned_motion_values = []

for file in file_list:
    if str(file).endswith(task_ww_filename + file_ext):
        ww_parsed_values.append(parse_timed_actions(parse_csv(file)))
    elif str(file).endswith(task_1d_filename + file_ext):
        oned_parsed_values.append(parse_timed_actions(parse_csv(file)))
    elif str(file).endswith(motion_ww_filename + file_ext):
        ww_motion_values.append(parse_csv(file))
    elif str(file).endswith(motion_1d_filename + file_ext):
        oned_motion_values.append(parse_csv(file))

ww_timed_actions = extract_timed_actions(ww_parsed_values)
oned_timed_actions = extract_timed_actions(oned_parsed_values)

ww_keypress_times = calculate_keypress_time(ww_timed_actions)
ww_keypress_times.sort()

oned_keypress_times = calculate_keypress_time(oned_timed_actions)
oned_keypress_times.sort()

print([item[0] for item in ww_keypress_times])
print([item[0] for item in oned_keypress_times])
print([item[1] for item in ww_keypress_times])
print([item[1] for item in oned_keypress_times])
print([item[2] for item in ww_keypress_times])
print([item[2] for item in oned_keypress_times])
print([item[3] for item in ww_keypress_times])
print([item[3] for item in oned_keypress_times])