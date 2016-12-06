# Motion Analysis Module

motion_ww_filename = "MotionRecordWatchInputToGlassActivity"
motion_1d_filename = "MotionRecordGlassOneDActivity"

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