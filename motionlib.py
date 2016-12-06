# Motion Analysis Module
import keynode

motion_ww_filename = "MotionRecordWatchInputToGlassActivity"
motion_1d_filename = "MotionRecordGlassOneDActivity"

label_drop = "drop"
label_multitouch = "multitouch"
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


# analyze a segment with the given keynode tree
# format: [ action, list of timestamps at which position entered to a new  ]
def analyze_segment(segment, keytree):
    # prune out multitouch segments
    for event in segment:
        if event[3] == action_multitouch:
            return label_multitouch

    # follow the keynode tree
    current_node = keytree
    prev_idx = 99999        # different value from return value of touch_area()
    timestamps = []
    for event in segment:
        child_idx = touch_area(event[1:3])
        if child_idx == -1:
            continue
        if prev_idx != child_idx:
            timestamps.append(event[0])
            if child_idx < 0 or child_idx >= 4:
                return label_drop
            if current_node.is_leaf():
                current_node = current_node.parent.children[child_idx]
            else:
                current_node = current_node.children[child_idx]
            prev_idx = child_idx

    return [current_node.action, timestamps]