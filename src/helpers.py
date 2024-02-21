import numpy as np
from typing import List
from models import Orientation
import math
import socket
import time
import json


def get_slope_intercept(axisreal_to_axisxgama:List[tuple]):
    """
    This function gets the relationship mapping between two axis from different coordinate systems.

    Example:
        xreal_to_xgama = [
            (-1.986089825630188*100, 50),  # Adjusted x value, original x value
            (-1.4845858812332153*100, 100),
            (-0.9858225584030151*100, 150),
            (-1.4873205423355103*100, 100),
            (-0.4857325553894043*100, 200)
        ]
        m,b = (0.9997576820030487, 248.5598673396752)
    """
    adjusted_array = np.array(axisreal_to_axisxgama)
    x_values = adjusted_array[:, 0]
    y_values = adjusted_array[:, 1]
    m, b = np.polyfit(x_values, y_values, 1)
    return m, b


def quaternion_to_euler(data: Orientation):
    x = data.x
    y = data.y
    z = data.z
    w = data.w

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    X = math.atan2(t0, t1)

    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    Y = math.asin(t2)

    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    Z = math.atan2(t3, t4)

    return [X, Y, Z]

def calculate_x_and_y_into_2d_plane(x:float, y:float, m_x=0.9997576820030487, b_x=248.5598673396752, m_y=1.001384757761485, b_y=100.55975739950252): # x: (0.9997576820030487, 248.5598673396752) y: (1.001384757761485, 100.55975739950252)
    # system of equations
    # y = m_x * x + b_x
    # y = m_y * x + b_y
    [x_2d, y_2d] = np.dot([[m_x, 0], [0, m_y]], [x, y]) + [b_x, b_y]                                                         
    return x_2d, y_2d


def udp_emitter(host='127.0.0.1', port=9876, x=0, y=0, z=0):
    """
    A UDP emitter that sends different x, y, z coordinates to the specified host and port every 5 seconds.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            message = f"[{x},{y},{z}]"
            
            sock.sendto(message.encode(), (host, port))

            print(f"Message sent: {message}")



def load_data(file_path:str = 'data/test_data.json'):
    """
    Load the data from a file and return it as a list of dictionaries.
    """
    with open(file_path, 'r') as file:
        content = file.read()
    return json.loads(content)