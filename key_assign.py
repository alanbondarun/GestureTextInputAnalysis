import motionlib

# dictionary: { 'key': frequency }, motion_weight: { 'motion': weight }
def ww_key_assign(freq_dic, motion_weight):
    key_total_weight = [(['tap0'], 0), (['tap1'], 0), (['tap2'], 0)]
    for i in range(3):
        for j in range(4):
            if i == j:
                continue
            key_description = ['area' + str(i), 'move' + str(j)]
            motion1 = motionlib.label_ww_motion[(i, j)]
            key_total_weight.append((key_description, motion_weight[motion1 + '1']))

    for i in range(3):
        for j in range(4):
            for k in range(4):
                if i == j or j == k:
                    continue
                key_description = ['area' + str(i), 'move' + str(j), 'move' + str(k)]
                motion1 = motionlib.label_ww_motion[(i, j)]
                motion2 = motionlib.label_ww_motion[(j, k)]
                key_total_weight.append((key_description, motion_weight[motion1 + '1'] + motion_weight[motion2 + '2']))

    key_total_weight.sort(key = lambda pair: pair[1])

    letter_freq_list = []
    for letter, freq in freq_dic.items():
        letter_freq_list.append((letter, freq))
    letter_freq_list.sort(reverse = True, key = lambda  pair: pair[1])

    letter_motions = []
    keys_iter = iter(key_total_weight)
    for letter, letter_freq in letter_freq_list:
        key_description, key_weight = next(keys_iter)
        letter_motions.append((letter, key_description))

    return letter_motions