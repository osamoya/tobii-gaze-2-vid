import argparse
import tobii_research as tr
import keyboard
import time
import csv

found_eyetrackers = tr.find_all_eyetrackers()
my_eyetracker = found_eyetrackers[0]
gaze_data_list = []

isDeviceActive=False
hotkey_start = 'ctrl + alt + r'
output_file_name = 'gaze_data.csv'
start_time = time.time()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Tobii Gaze Recorder")
    parser.add_argument('--output', type=str, default='gaze_data.csv',
                        help='Output CSV file name (default: gaze_data.csv)')
    parser.add_argument('--hotkey', type=str, default='ctrl + alt + r',
                        help='Hotkey for starting/stopping recording (default: ctrl + alt + r)')
    return parser.parse_args()


def gaze_data_callback(gaze_data): 
    gaze_data_list.append(gaze_data)

def stream_start():
    global isDeviceActive
    if isDeviceActive:
        #print('still active')
        stream_end_and_output()
    else:
        print('stream start')
        my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)
        isDeviceActive=True
    

def stream_end():
    print('stream end')
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

def stream_end_and_output():
    global isDeviceActive
    stream_end()
    outputCSV()
    isDeviceActive = False

def outputCSV():
    with open(output_file_name, 'w', newline='') as csvfile:
        record_start_time=gaze_data_list[0]["system_time_stamp"]
        fieldnames = ['time_stamp','left_eye_x', 'left_eye_y', 'right_eye_x', 'right_eye_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data in gaze_data_list:
            time_stamp=(start_time + (data["system_time_stamp"]-record_start_time)/(10**6))
            # time_stamp=data["system_time_stamp"]
            #time_stamp=(start_time + (data["system_time_stamp"]-record_start_time))
            left_eye_x = data['left_gaze_point_on_display_area'][0]
            left_eye_y = data['left_gaze_point_on_display_area'][1]
            right_eye_x = data['right_gaze_point_on_display_area'][0]
            right_eye_y = data['right_gaze_point_on_display_area'][1]
            # csv書き込み
            writer.writerow({
                'time_stamp':time_stamp,
                'left_eye_x': left_eye_x,
                'left_eye_y': left_eye_y,
                'right_eye_x': right_eye_x,
                'right_eye_y': right_eye_y
            })

# メイン処理の冒頭で引数を解析
args = parse_arguments()
print(f"args = {args}")

output_file_name = args.output
hotkey_start = args.hotkey

print('activate...')
keyboard.add_hotkey(hotkey_start,stream_start)
#keyboard.add_hotkey('o',stream_end_and_output)
keyboard.wait('ctrl + alt + e')
print('end...')