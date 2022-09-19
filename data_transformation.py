import os
import numpy as np
from numpy.lib.function_base import vectorize
import pandas as pd

def find_next_down(array):
    for index, line in enumerate(np.array(array)):
        if(line[1] == 'KeyDown'):
            return line, index+1
    return [0, 0, 0], 0

def find_up_key(array, letter):
    for index, line in enumerate(np.array(array)):
        if(line[0] == letter and line[1] == 'KeyUp'):
            return line, index+1
    return ([0, 0, 0], 0)

def prepare_vectors(from_file_lines, file_number):
    vectors = []
    for (index, line) in enumerate(np.array(from_file_lines)): 
        if(line[1]=='KeyDown' and line[2] != 0):
            Id1 = line[0]

            next_key_down, next_down_index = find_next_down(from_file_lines[index+1:]) 
            next_down_index += index 

            Id2 = next_key_down[0]
            press_press_time = next_key_down[2] - line[2] 

            up_key, up_key_index = find_up_key(from_file_lines[index+1:], line[0]) 
            up_key_index += index
            hold_time = up_key[2] - line[2]

            next_pair_key_up, _ = find_up_key(from_file_lines[next_down_index+1:], next_key_down[0])
            hold2_time = next_pair_key_up[2] - next_key_down[2]

            press_release_time = next_pair_key_up[2] - line[2]

            vector = [file_number, Id1, Id2, hold_time, hold2_time, press_release_time, press_press_time]
            isCorrect = all(x > 0 for x in vector[3:])
            if(isCorrect == True):
                from_file_lines.iloc[index,2] = 0
                from_file_lines.iloc[up_key_index,2] = 0
                vectors.append(vector)
    return vectors   

# file_numbers = range(11, 60)
unprocessed_files = os.listdir("{}/{}".format("data_preparation", "free_input_unprocessed_data"))

for file in unprocessed_files: 
    print(os.getcwd())
    # file_name = "00" + str(file_number) + "000.txt"
    path = "{}/{}/{}".format("data_preparation", "free_input_unprocessed_data", file)
    df = pd.read_csv(path, sep=" ", header = None)
    processed = prepare_vectors(df, file[:3])

    directory = "{}/{}".format("data_preparation", "free_input_processed_data_second_part")
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(directory)

    f=open(f"{file}",'a')

    for line in processed: 
        np.savetxt(f, line,fmt ='%s' , newline=", ")
        f.write("\n")
    f.close()
    os.chdir("../..")