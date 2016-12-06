# Motion Analysis Module
import keynode

motion_ww_filename = "MotionRecordWatchInputToGlassActivity"
motion_1d_filename = "MotionRecordGlassOneDActivity"

label_drop = "drop"
label_multitouch = "multitouch"
label_horiz_motion = "h"
label_verti_motion = "v"
label_diag_motion = "d"
action_multitouch = 261

ww_screen_dimens = (213.0, 213.0)
ww_deadzone_ratio = 0.4

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
def touch_area(position):
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

def motion_from_areas(prev_area, current_area):
    if not (0 <= prev_area < 4):
        return None
    if not (0 <= current_area < 4):
        return None
    if prev_area == current_area:
        return None

    if abs(prev_area - current_area) == 1:
        if (prev_area == 1 and current_area == 2) or (prev_area == 2 and current_area == 1):
            return label_diag_motion
        return label_horiz_motion
    if abs(prev_area - current_area) == 2:
        return label_verti_motion
    return label_diag_motion

# analyze a segment with the given keynode tree
# format: [ action, list of timestamps at which position entered to a new,
#               list of [kind of motion, time interval] ]
# in the time interval list of motions, the redundant motions are removed (e.g. v -> h -> h for entering 'o')
def analyze_segment(segment, keytree):
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
        child_idx = touch_area(event[1:3])
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
                    motions.append([motion_from_areas(prev_idx, child_idx), event[0] - timestamps[-2]])
            prev_idx = child_idx

    return [current_node.action, timestamps, motions]

# { key: { 'h': [time intervals], 'v': [time_intervals], 'd': [time_intervals] } }
def aggregate_motion_times(segmented_files, keytree):
    key_dict = {}
    for segment_list in segmented_files:
        for segment in segment_list:
            anal_res = analyze_segment(segment, keytree)
            if anal_res[0] in key_dict:
                for motion_record in anal_res[2]:
                    if motion_record[0] == label_horiz_motion:
                        key_dict[anal_res[0]][label_horiz_motion].append(motion_record[1])
                    elif motion_record[0] == label_verti_motion:
                        key_dict[anal_res[0]][label_verti_motion].append(motion_record[1])
                    elif motion_record[0] == label_diag_motion:
                        key_dict[anal_res[0]][label_diag_motion].append(motion_record[1])
            else:
                horizs = []
                verts = []
                diags = []
                for motion_record in anal_res[2]:
                    if motion_record[0] == label_horiz_motion:
                        horizs.append(motion_record[1])
                    elif motion_record[0] == label_verti_motion:
                        verts.append(motion_record[1])
                    elif motion_record[0] == label_diag_motion:
                        diags.append(motion_record[1])
                key_dict[anal_res[0]] = { label_horiz_motion: horizs, label_verti_motion: verts,
                                          label_diag_motion: diags }

    return key_dict

def aggregate_motion_times_rtable(segmented_files, keytree):
    rtable = [['key', 'motion', 'time']]

    motion_times = aggregate_motion_times(segmented_files, keytree)
    for key in motion_times.keys():
        if key == '' or key == label_multitouch:
            continue
        for timeval in motion_times[key][label_horiz_motion]:
            rtable.append([key, label_horiz_motion, timeval])
        for timeval in motion_times[key][label_verti_motion]:
            rtable.append([key, label_verti_motion, timeval])
        for timeval in motion_times[key][label_diag_motion]:
            rtable.append([key, label_diag_motion, timeval])
    return rtable


# (num-multi, num-empty)
def num_multi_versus_empty(segmented_files, keytree):
    count = [[0, []], [0, []]]
    for segment_list in segmented_files:
        for segment in segment_list:
            anal_res = analyze_segment(segment, keytree)
            if anal_res[0] == label_multitouch:
                count[0][0] += 1
                count[0][1].append(segment[-1][0] - segment[0][0])
            elif anal_res[0] == '':
                count[1][0] += 1
                count[1][1].append(segment[-1][0] - segment[0][0])
    count[0][1] = sum(count[0][1]) / len(count[0][1])
    count[1][1] = sum(count[1][1]) / len(count[1][1])
    return count