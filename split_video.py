import pandas as pd
import argparse
import os

# parse arguments input_video, input_csv and output_folder
def parse_arguments():
    parser = argparse.ArgumentParser(description='Split video based on CSV input.')
    parser.add_argument('--input_folder', type=str, help='Path to the input folder')
    parser.add_argument('--input_csv', type=str, help='Path to the input CSV file')
    parser.add_argument('--output_folder', type=str, help='Path to the output folder')
    return parser.parse_args()

args = parse_arguments()


df = pd.read_csv(args.input_csv)

# Create output folder if it does not exist
if not os.path.exists(args.output_folder):
    os.makedirs(args.output_folder)

def string_to_seconds(s):
    start_hours = 0
    start_minutes = 0
    start_seconds = 0
    
    if len(s.split(':')) == 3:
        start_hours, start_minutes, start_seconds = map(int, s.split(':'))
    elif len(s.split(':')) == 2:
        start_minutes, start_seconds = map(int, s.split(':'))
    elif len(s.split(':')) == 1:
        start_seconds = int(s)
    
    return start_hours * 3600 + start_minutes * 60 + start_seconds

# calculate the time difference beteween two string XX:YY and AA:BB in seconds
def time_difference(start, end):
    start_total_seconds = string_to_seconds(start)
    end_total_seconds = string_to_seconds(end)
    return end_total_seconds - start_total_seconds

for i, row in df.iterrows():
    print(row)
    # get the ffmpeg command to extract a clip from a video and reencoding it in x264 with crf 18
    video = os.path.join(args.input_folder, row["video"])
    start_time = row['start_time']
    end_time = row['end_time']
    t = time_difference(start_time, end_time)
    name = row["name"]
    output_file = f"{args.output_folder}/{name}.mkv"
    if not os.path.exists(output_file):
        ffmpeg_command = f"ffmpeg -ss '{start_time}' -i '{video}' -t '{t}' -c:v copy -c:a copy '{output_file}'"
        print(ffmpeg_command)
        os.system(ffmpeg_command)


for i, row in df.iterrows():
    name = row["name"]
    output_file = f"{args.output_folder}/{name}.mkv"
    if not os.path.exists(output_file):
        print(f"Error: {output_file} was not created")