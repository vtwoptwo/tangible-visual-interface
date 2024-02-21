
import time
from helpers import get_slope_intercept, quaternion_to_euler, calculate_x_and_y_into_2d_plane, udp_emitter, load_data
from models import Input, desired_output


def main(data:str = 'data/test_data.json'): 
    x_previous = 0
    y_previous = 0
    treshold = 1
    structures = load_data(file_path=data)
    for index, data in enumerate(structures, start=1):
        # process the data
        try:
            input_data = Input().create(data)
            desired_output_t = desired_output().create(input_data, quaternion_to_euler(input_data.pose.orientation))
            x,y = calculate_x_and_y_into_2d_plane(x=desired_output_t.x, y=desired_output_t.y)
            if abs(x - x_previous) > treshold or abs(y - y_previous) > treshold:
                x_previous = x
                y_previous = y
                udp_emitter(x=x, y=y, z=desired_output_t.z)
                print(f"Structure {index}:", x, y, desired_output_t.z)
                time.sleep(0.1)
            else: 
                continue

        except:
            print(f"Structure {index}:", "Error processing data")


if __name__ == "__main__":
    # args parser file path
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--file', type=str, help='file path to the data')
    args = parser.parse_args()
    data = args.file

    main(data)

