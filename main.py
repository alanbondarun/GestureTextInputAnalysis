from pathlib import Path
from anallib import *
from motionlib import *
from keynode import *
from key_assign import *

file_list = [x for x in Path(res_directory).iterdir() if x.is_file()]

ww_parsed_values = []
oned_parsed_values = []
ww_motion_values = []
oned_motion_values = []

for file in file_list:
    if str(file).endswith(task_ww_filename + file_ext):
        ww_parsed_values.append(postprocess_task_values(parse_csv(file, start_from=3)))
    elif str(file).endswith(task_1d_filename + file_ext):
        oned_parsed_values.append(postprocess_task_values(parse_csv(file, start_from=3)))
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

# aggregate all blocks & people and generate key press time information
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

# group timed actions by people and generate key press time information
'''
ww_keytime_by_person = []
for ta_by_person in extract_timed_actions(ww_parsed_values, by_person = True):
    ww_keytime_by_person.append(calculate_keypress_time(ta_by_person))
oned_keytime_by_person = []
for ta_by_person in extract_timed_actions(oned_parsed_values, by_person = True):
    oned_keytime_by_person.append(calculate_keypress_time(ta_by_person))

print(ww_keytime_by_person)
print(oned_keytime_by_person)
'''

# group timed actions by block and generate key press time information
'''
ww_keytime_by_block = []
for ta_by_block in extract_timed_actions_byblock(ww_parsed_values):
    ww_keytime_by_block.append(calculate_keypress_time(ta_by_block))
oned_keytime_by_block = []
for ta_by_block in extract_timed_actions_byblock(oned_parsed_values):
    oned_keytime_by_block.append(calculate_keypress_time(ta_by_block))

print(ww_keytime_by_block[0])
print(ww_keytime_by_block[-1])
print(oned_keytime_by_block[0])
print(oned_keytime_by_block[-1])
'''

# calculate error rates of each input character across all blocks and people
'''
print(aggregate_errors(ww_parsed_values))
print(aggregate_errors(oned_parsed_values))
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
'''
print(aggregate_motion_times_rtable(ww_segmented_files, ww_keytree))
'''

# multitouch vs. void part analysis
'''
print(num_multi_versus_empty(ww_segmented_files, ww_keytree, False))
print(num_multi_versus_empty(oned_segmented_files, oned_keytree, True))
'''

# key assignment
print(ww_key_assign(
    {
        'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68, 'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
        'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88, 'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11,
        'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49, 'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
        'j': 0.10, 'z': 0.07
    },
    {
        'da1': 1213.38, 'db1': 746.22, 'dc1': 961.36, 'dd1': 1131.00,
        'da2': 1213.38, 'db2': 746.22, 'dc2': 961.36, 'dd2': 1131.00,
        'hl1': 901.51, 'hr1': 773.46, 'vb1': 741.38, 'vt1': 896.92,
        'hl2': 691.05, 'hr2': 684.87, 'vb2': 643.62, 'vt2': 668.75
    }
))