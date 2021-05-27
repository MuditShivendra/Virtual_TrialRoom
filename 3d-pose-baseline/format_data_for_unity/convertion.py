import json


def convert_list_to_str(l):
    return '[ ' + ' '.join(map(str, l)) + ' ]'


with open('./3d_data.json', 'r') as json_file:
    data = json.load(json_file)
    out_data = {}       # format  --->  {frame_no : [[x1...x32][y1...y32][z1...z32]]}
    # LOOP OVER FRAME
    for frame_no in data.keys():
        x = []
        y = []
        z = []
        frame = data[frame_no]
        # LOOP OVER SKELETON POINTS IN A FRAME
        for joint_no in frame.keys():
            joint_position = frame[joint_no]['translate']
            x.append(joint_position[0])
            y.append(joint_position[1])
            z.append(joint_position[2])

        # merge x, y, z
        xyz = '[['
        xyz += convert_list_to_str(x) + '\n'
        xyz += convert_list_to_str(y) + '\n'
        xyz += convert_list_to_str(z) + ']]'

        # save out_data to file
        with open('./openPose_rig_input/3d_data'+str(frame_no)+'.txt', 'w+') as outfile:
            outfile.write(xyz)

print('Done')