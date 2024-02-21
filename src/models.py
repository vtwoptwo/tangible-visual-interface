from dataclasses import dataclass
import math

@dataclass
class Orientation:
    x: float
    y: float
    z: float
    w: float

@dataclass
class desired_output:
    x: float
    y: float
    z: float

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def create(self, data, euler: list):
        self.x = data.pose.position.x
        self.y = data.pose.position.y
        self.z = euler[2]
        return self
    
@dataclass
class stamp:
    secs: int
    nsecs: int


@dataclass
class Header:
    seq: int
    stamp: stamp
    frame_id: str

@dataclass
class Position: 
    x: float
    y: float
    z: float


@dataclass
class Pose:
    position: Position
    orientation: Orientation

@dataclass
class Input:
    header: Header
    pose: Pose

    def __init__(self):
        self.header = Header(0, stamp(0, 0), " ")
        self.pose = Pose(Position(0, 0, 0), Orientation(0, 0, 0, 0))

    def create(self, data: dict):
        self.header.seq = data['header']['seq']
        self.header.stamp.secs = data['header']['stamp']['secs']
        self.header.stamp.nsecs = data['header']['stamp']['nsecs']
        self.header.frame_id = data['header']['frame_id']
        self.pose.position.x = data['pose']['position']['z'] * 100
        self.pose.position.y = data['pose']['position']['x'] * 100
        self.pose.position.z = data['pose']['position']['y'] * 100
        self.pose.orientation.x = data['pose']['orientation']['x'] * 100
        self.pose.orientation.y = data['pose']['orientation']['y'] * 100
        self.pose.orientation.z = data['pose']['orientation']['z'] * 100
        self.pose.orientation.w = data['pose']['orientation']['w'] * 100
        return self    
