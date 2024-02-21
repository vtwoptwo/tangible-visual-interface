import re
import json

def parse_data(text):
    # Define the data structure to be filled
    data = {
        "header": {
            "seq": 664906,  # stay the same because we are not using them in the example 
            "stamp": {
                "secs": 1708455886,
                "nsecs": 248592461
            },
            "frame_id": "world"
        },
        "pose": {
            "position": {},
            "orientation": {}
        }
    }
    
    # Regular expressions for matching the key components and their values
    position_regex = re.compile(r"position:\s*x:\s*([-\d\.]+)\s*y:\s*([-\d\.]+)\s*z:\s*([-\d\.]+)")
    orientation_regex = re.compile(r"orientation:\s*x:\s*([-\d\.]+)\s*y:\s*([-\d\.]+)\s*z:\s*([-\d\.]+)\s*w:\s*([-\d\.]+)")

    # Search for position and orientation data in the text
    position_match = position_regex.search(text)
    orientation_match = orientation_regex.search(text)
    
    if position_match:
        data['pose']['position'] = {
            "x": float(position_match.group(1)),
            "y": float(position_match.group(2)),
            "z": float(position_match.group(3))
        }
    
    if orientation_match:
        data['pose']['orientation'] = {
            "x": float(orientation_match.group(1)),
            "y": float(orientation_match.group(2)),
            "z": float(orientation_match.group(3)),
            "w": float(orientation_match.group(4))
        }
    
    return data


def parse_ros_topic_msg_from_txt(file_path:str = 'data.txt'):
    with open(file_path, 'r') as file:
        content = file.read()
    # Split the content by '---', preprocess, and parse each part
    structures = [parse_data(part) for part in content.split('---') if part.strip()]
    # save the data into a file
    with open('output.json', 'w') as file:
        json.dump(structures, file, indent=4)
        
    # for index, data in enumerate(structures, start=1):
    #     print(f"Structure {index}:", data)

