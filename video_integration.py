import argparse
import csv
import cv2
import numpy as np
from tqdm import tqdm


def parse_arguments():
    parser = argparse.ArgumentParser(description="Gaze Data Interpolation")
    parser.add_argument('--csv', type=str, required=True, help='csv file path')
    parser.add_argument('--movie', type=str, required=True, help='movie file path')
    parser.add_argument('--output', type=str, required=True, help='Output mp4 file path')
    return parser.parse_args()

def main():
    args = parse_arguments()
    print(f"args = {args}")
    interpolated_csv_name = args.csv
    movie_name = args.movie
    output_mp4_name = args.output

    with open(interpolated_csv_name) as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    NUM_FRAME_CSV=len(l)
    print(NUM_FRAME_CSV)

    cap = cv2.VideoCapture(movie_name)
    NUM_FRAME_MOVIE=cap.get(cv2.CAP_PROP_FRAME_COUNT)
    print(cap.isOpened())
    ret, frame = cap.read()
    print(ret)
    print(frame.shape)
    print(type(frame))
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    print(cap.get(cv2.CAP_PROP_POS_FRAMES))


    CSV_OFFSET_SECOND = 1
    # csv_counter=int(CSV_OFFSET_SECOND * (60))
    csv_counter = 1
    #tqdm_MAX = NUM_FRAME_CSV if NUM_FRAME_CSV<NUM_FRAME_MOVIE else int(NUM_FRAME_MOVIE) # TODO：ここの処理ダメかも．あとで検証する
    print('start...')
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # フレームの幅
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # フレームの高さ
    fps = float(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 動画のコーデックを指定
    out = cv2.VideoWriter(output_mp4_name, fourcc, fps, (frame_width, frame_height))

    #for i in tqdm(range(csv_counter,tqdm_MAX)):
    for i in tqdm(range(csv_counter, NUM_FRAME_CSV)):
        ret, frame = cap.read()
        if not ret:
            print('読み込みでえらりました,i=',i)
            break
        Left_eye_x=float(l[i][1])
        Left_eye_y=float(l[i][2])
        Right_eye_x=float(l[i][3])
        Right_eye_y=float(l[i][4])

        is_Left_eye_open=(not np.isnan(Left_eye_x) and not np.isnan(Left_eye_y))
        is_Right_eye_open=(not np.isnan(Right_eye_x) and not np.isnan(Right_eye_y))

        if(is_Left_eye_open):
            cv2.circle(frame, (int(Left_eye_x*cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(Left_eye_y*cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), radius=16, color=(255,0,0))
        if(is_Right_eye_open):
            cv2.circle(frame, (int(Right_eye_x*cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(Right_eye_y*cap.get(cv2.CAP_PROP_FRAME_HEIGHT))), radius=16, color=(0,0,255))
        if(is_Left_eye_open or is_Right_eye_open):
                #ぼやっと円を書いてみたい
                if(is_Left_eye_open and is_Right_eye_open):
                    eye_x=(Left_eye_x+Right_eye_x)/2
                    eye_y=(Left_eye_y+Right_eye_y)/2
                elif(is_Left_eye_open and not is_Right_eye_open):# 右目が閉じている
                    eye_x=Left_eye_x
                    eye_y=Left_eye_y
                elif(not is_Left_eye_open and is_Right_eye_open):# 左目が閉じている
                    eye_x=Right_eye_x
                    eye_y=Right_eye_y
                cv2.circle(frame,(int(eye_x*cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(eye_y*cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),157,color=(255,255,255))
                cv2.circle(frame,(int(eye_x*cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(eye_y*cap.get(cv2.CAP_PROP_FRAME_HEIGHT))),162,color=(0,0,0))
        # frames.append(frame)
        out.write(frame)
    out.release()
    print('end...')


if __name__ == "__main__":
    main()
