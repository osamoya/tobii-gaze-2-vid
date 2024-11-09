import csv
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Gaze Data Interpolation")
    parser.add_argument('--input', type=str, required=True, help='Input CSV file path')
    parser.add_argument('--output', type=str, required=True, help='Output CSV file path')
    return parser.parse_args()


def main():
    args = parse_arguments()

    # CSV補間
    with open(args.input) as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    csv_after=[]
    for i,row in enumerate(l,start=1):
        if i<len(l)-1:
            current_row = l[i]
            next_row = l[i + 1]
            diff=float(next_row[0])-float(current_row[0])
            num_betoween_frame=round(diff/(1/60))-1
            # print(current_row[0],',',next_row[0],'diff=',diff,'nbf=',num_betoween_frame)
            if diff>=float(0.03) :
                csv_after.append(l[i])
                # print(num_betoween_frame,'Fの欠損')
                for n in range(num_betoween_frame):
                    # print('i=',i,',n=',n)
                    new_1frame=[]

                    for x in range(5):

                        if l[i][x]=='nan' and l[i+1][x]=='nan':
                            new_1frame.append('nan')
                        elif l[i][x]=='nan':
                            new_1frame.append(l[i+1][x])
                        elif l[i+1][x]=='nan':
                            new_1frame.append(l[i][x])
                        else:
                            now=float(l[i][x])
                            next=float(l[i+1][x])
                            tmp=((num_betoween_frame-n)*now+(n+1)*next)/(num_betoween_frame+1)
                            new_1frame.append(tmp)
                    csv_after.append(new_1frame)
            else :
                csv_after.append(l[i])
    csv_after.append(l[-1])

    with open(args.output, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=l[0])
        writer.writeheader()
        for data_after in csv_after:
            writer.writerow({
                    'time_stamp':data_after[0],
                    'left_eye_x': data_after[1],
                    'left_eye_y': data_after[2],
                    'right_eye_x': data_after[3],
                    'right_eye_y': data_after[4]
                })

    print(f"Interpolation complete. Output written to {args.output}")

if __name__ == "__main__":
    main()
