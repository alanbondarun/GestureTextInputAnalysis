# Motion Analysis Module
import keynode
import statistics

motion_ww_filename = "MotionRecordWatchInputToGlassActivity"
motion_1d_filename = "MotionRecordGlassOneDActivity"

label_drop = "drop"
label_multitouch = "multitouch"
label_horiz_motion = "h"
label_verti_motion = "v"
label_diag_motion = "d"
label_ww_motion = {
    (0, 1): label_horiz_motion + "l", (0, 2): label_verti_motion + "b", (0, 3): label_diag_motion + "a",
    (1, 0): label_horiz_motion + "r", (1, 2): label_diag_motion + "b", (1, 3): label_verti_motion + "b",
    (2, 0): label_verti_motion + "t", (2, 1): label_diag_motion + "c", (2, 3): label_horiz_motion + "l",
    (3, 0): label_diag_motion + "d", (3, 1): label_verti_motion + "t", (3, 2): label_horiz_motion + "r"
}
action_multitouch = 261

ww_screen_dimens = (213.0, 213.0)
ww_deadzone_ratio = 0.4

oned_screen_dimens = (1366, 187)

'''
    motion event data: [timestamp:long, x_position:float, y_position:float, action:int]
    convert data type of each motion event data from string to [int, float, float, int]
    :param raw_list list of event data
    :return converted list of event data
'''
def convert_to_numeric(raw_list):
    converted_file = []
    for raw_data in raw_list:
        if len(raw_data) == 4:
            converted_file.append([int(raw_data[0]), float(raw_data[1]), float(raw_data[2]), int(raw_data[3])])
    return converted_file

# segment motion events with touch down(action=0) and touch up (action=1)
def segment_motion_rawdata(raw_list):
    segmented_list = []
    segment = []
    for raw_data in raw_list:
        segment.append(raw_data)
        if raw_data[3] == 1:
            segmented_list.append(segment)
            segment = []

    return segmented_list

# given a coordinate, calculate the area number
# return: area number in [0, 3), -1 if the touch area is in the dead zone or -2 if out of the touch area
def touch_area_ww(position):
    relx = position[0] / ww_screen_dimens[0]
    rely = position[1] / ww_screen_dimens[1]
    if 0 <= relx <= 1 and 0 <= rely <= 1:
        if relx <= ww_deadzone_ratio:
            if rely <= ww_deadzone_ratio:
                return 0
            elif rely >= 1 - ww_deadzone_ratio:
                return 2
            else:
                return -1
        elif relx >= 1 - ww_deadzone_ratio:
            if rely <= ww_deadzone_ratio:
                return 1
            elif rely >= 1 - ww_deadzone_ratio:
                return 3
            else:
                return -1
        else:
            return -1
    return -2


# given a coordinate, calculate the area number
# return: area number in [0, 3), -1 if the touch area is in the dead zone or -2 if out of the touch area
def touch_area_1d(position):
    relx = position[0] / oned_screen_dimens[0]
    if 0 <= relx < 1:
        return int(relx * 4.0)
    elif relx >= 1:
        return 3
    return -2

def ww_motion_from_areas(prev_area, current_area):
    if not (0 <= prev_area < 4):
        return None
    if not (0 <= current_area < 4):
        return None
    if prev_area == current_area:
        return None
    return label_ww_motion[(prev_area, current_area)]

# analyze a segment with the given keynode tree
# format: [ action, list of timestamps at which position entered to a new,
#               list of [kind of motion, time interval] ]
# in the time interval list of motions, the redundant motions are removed (e.g. v -> h -> h for entering 'o')
def analyze_segment_ww(segment, keytree):
    # prune out multitouch segments
    for event in segment:
        if event[3] == action_multitouch:
            return [label_multitouch, [], []]

    # follow the keynode tree
    current_node = keytree
    prev_idx = 99999        # different value from return value of touch_area()
    timestamps = []
    motions = []
    for event in segment:
        child_idx = touch_area_ww(event[1:3])
        if child_idx == -1:
            continue
        if prev_idx != child_idx:
            timestamps.append(event[0])
            if child_idx < 0 or child_idx >= 4:
                break
            if current_node.is_leaf():
                if len(motions) >= 1:
                    motions = motions[:-1]
                current_node = current_node.parent.children[child_idx]
            else:
                current_node = current_node.children[child_idx]
                if len(timestamps) >= 2:
                    len_motions = len(motions) + 1
                    motions.append([ww_motion_from_areas(prev_idx, child_idx) + str(len_motions), event[0] - timestamps[-2]])
            prev_idx = child_idx

    return [current_node.action, timestamps, motions]


# analyze a segment with the given keynode tree
# format: [action, input_time]
def analyze_segment_1d(segment, keytree):
    # prune out multitouch segments
    for event in segment:
        if event[3] == action_multitouch:
            return [label_multitouch, [], []]

    # follow the keynode tree
    current_node = keytree
    prev_idxes = []
    for event in segment:
        child_idx = touch_area_1d(event[1:3])
        if child_idx == -1:
            continue
        if len(prev_idxes) <= 0 or prev_idxes[-1] != child_idx:
            if child_idx < 0 or child_idx >= 4:
                break
            if current_node.is_leaf():
                current_node = current_node.parent.children[child_idx]
            elif len(prev_idxes) >= 2 and (child_idx - prev_idxes[-1]) * (prev_idxes[-1] - prev_idxes[-2]) == 1:
                current_node = current_node.parent.children[child_idx]
            else:
                current_node = current_node.children[child_idx]

            prev_idxes.append(child_idx)

    return [current_node.action, segment[-1][0] - segment[0][0]]

# { key: { 'h': [time intervals], 'v': [time_intervals], 'd': [time_intervals] } }
def aggregate_motion_times_ww(segmented_files, keytree):
    key_dict = {}
    for segment_list in segmented_files:
        for segment in segment_list:
            anal_res = analyze_segment_ww(segment, keytree)
            if anal_res[0] in key_dict:
                for motion_record in anal_res[2]:
                    if motion_record[0][:len(label_horiz_motion)] == label_horiz_motion:
                        key_dict[anal_res[0]][label_horiz_motion].append(motion_record[1])
                    elif motion_record[0][:len(label_verti_motion)] == label_verti_motion:
                        key_dict[anal_res[0]][label_verti_motion].append(motion_record[1])
                    elif motion_record[0][:len(label_diag_motion)] == label_diag_motion:
                        key_dict[anal_res[0]][label_diag_motion].append(motion_record[1])
            else:
                horizs = []
                verts = []
                diags = []
                for motion_record in anal_res[2]:
                    if motion_record[0][:len(label_horiz_motion)] == label_horiz_motion:
                        horizs.append(motion_record[1])
                    elif motion_record[0][:len(label_verti_motion)] == label_verti_motion:
                        verts.append(motion_record[1])
                    elif motion_record[0][:len(label_diag_motion)] == label_diag_motion:
                        diags.append(motion_record[1])
                key_dict[anal_res[0]] = { label_horiz_motion: horizs, label_verti_motion: verts,
                                          label_diag_motion: diags }

    return key_dict

def aggergate_motion_times_1d(segmented_files, keytree):
    key_dict = {}
    for segment_list in segmented_files:
        for segment in segment_list:
            anal_res = analyze_segment_1d(segment, keytree)
            if anal_res[0] in key_dict:
                key_dict[anal_res[0]].append(anal_res[1])
            else:
                key_dict[anal_res[0]] = [anal_res[1]]

    return key_dict

def aggregate_motion_times_rtable(segmented_files, keytree):
    rtable = [['key', 'motion', 'time']]

    for segment_list in segmented_files:
        for segment in segment_list:
            anal_res = analyze_segment_ww(segment, keytree)
            for motion_record in anal_res[2]:
                rtable.append([anal_res[0], motion_record[0], motion_record[1]])
    return rtable


# [[num-multi, average-time, stdev], [num-empty, average-time, stdev]]
def num_multi_versus_empty(segmented_files, keytree, is_oned):
    multi_time_list = []
    null_time_list = []
    for segment_list in segmented_files:
        for segment in segment_list:
            if is_oned:
                anal_res = analyze_segment_1d(segment, keytree)
            else:
                anal_res = analyze_segment_ww(segment, keytree)
            if anal_res[0] == label_multitouch:
                multi_time_list.append(segment[-1][0] - segment[0][0])
            elif anal_res[0] == '':
                null_time_list.append(segment[-1][0] - segment[0][0])

    count = []
    count.append([len(multi_time_list), sum(multi_time_list) / len(multi_time_list), statistics.stdev(multi_time_list)])
    count.append([len(null_time_list), sum(null_time_list) / len(null_time_list), statistics.stdev(null_time_list)])
    return count