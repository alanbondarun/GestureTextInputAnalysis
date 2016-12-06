from pathlib import Path
from anallib import *
from motionlib import *
from keynode import *

file_list = [x for x in Path(res_directory).iterdir() if x.is_file()]

ww_parsed_values = []
oned_parsed_values = []
ww_motion_values = []
oned_motion_values = []

for file in file_list:
    if str(file).endswith(task_ww_filename + file_ext):
        ww_parsed_values.append(parse_timed_actions(parse_csv(file, start_from=3)))
    elif str(file).endswith(task_1d_filename + file_ext):
        oned_parsed_values.append(parse_timed_actions(parse_csv(file, start_from=3)))
    elif str(file).endswith(motion_ww_filename + file_ext):
        ww_motion_values.append(convert_to_numeric(parse_csv(file)))
    elif str(file).endswith(motion_1d_filename + file_ext):
        oned_motion_values.append(convert_to_numeric(parse_csv(file)))

ww_timed_actions = extract_timed_actions(ww_parsed_values)
oned_timed_actions = extract_timed_actions(oned_parsed_values)

ww_keypress_times = calculate_keypress_time(ww_timed_actions)
ww_keypress_times.sort()

oned_keypress_times = calculate_keypress_time(oned_timed_actions)
oned_keypress_times.sort()

'''
print([item[0] for item in ww_keypress_times])
print([item[0] for item in oned_keypress_times])
print([item[1] for item in ww_keypress_times])
print([item[1] for item in oned_keypress_times])
print([item[2] for item in ww_keypress_times])
print([item[2] for item in oned_keypress_times])
print([item[3] for item in ww_keypress_times])
print([item[3] for item in oned_keypress_times])
'''

ww_segmented_files = []
for raw_file in ww_motion_values:
    ww_segmented_files.append(segment_motion_rawdata(raw_file))
oned_segmented_files = []
for raw_file in oned_motion_values:
    oned_segmented_files.append(segment_motion_rawdata(raw_file))

ww_keytree = KeyNode.loadFromFile("./json/key_value_watch_3area_opt_2.json")
oned_keytree = KeyNode.loadFromFile("./json/key_value_oned_opt.json")

# WatchWrite segment analysis
print(aggregate_motion_times_rtable(ww_segmented_files, ww_keytree))

# multitouch vs. void part analysis
print(num_multi_versus_empty(ww_segmented_files, ww_keytree))
print(num_multi_versus_empty(oned_segmented_files, oned_keytree))