from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
import time

# Section 1.4 - final simulated candidate -> physical robot
# Example physical-run values (half or less of the simulated amplitudes).
HEAD_YAW = 5                 # degrees
ANTENNA_AMPLITUDE = 0.15     # radians
MOVE_DURATION = 1.0          # seconds


def stage(name):
    print(f"[STAGE] {name}", flush=True)


with ReachyMini() as mini:
    mini.enable_motors()
    mini.wake_up()

    stage("NEUTRAL_START")
    mini.goto_target(
        head=create_head_pose(yaw=0, pitch=0, degrees=True),
        antennas=[0.0, 0.0],
        duration=1.0,
    )
    time.sleep(0.5)

    stage("HEAD_LEFT")
    mini.goto_target(
        head=create_head_pose(yaw=HEAD_YAW, pitch=0, degrees=True),
        duration=MOVE_DURATION,
    )
    time.sleep(0.5)

    stage("HEAD_RIGHT")
    mini.goto_target(
        head=create_head_pose(yaw=-HEAD_YAW, pitch=0, degrees=True),
        duration=MOVE_DURATION,
    )
    time.sleep(0.5)

    stage("HEAD_CENTER")
    mini.goto_target(
        head=create_head_pose(yaw=0, pitch=0, degrees=True),
        duration=MOVE_DURATION,
    )
    time.sleep(0.5)

    stage("ANTENNAS_OUT")
    mini.goto_target(
        antennas=[ANTENNA_AMPLITUDE, -ANTENNA_AMPLITUDE],
        duration=MOVE_DURATION,
    )
    time.sleep(0.5)

    stage("ANTENNAS_REVERSE")
    mini.goto_target(
        antennas=[-ANTENNA_AMPLITUDE, ANTENNA_AMPLITUDE],
        duration=MOVE_DURATION,
    )
    time.sleep(0.5)

    stage("RETURN_NEUTRAL")
    mini.goto_target(
        head=create_head_pose(yaw=0, pitch=0, degrees=True),
        antennas=[0.0, 0.0],
        duration=MOVE_DURATION,
    )

    stage("DONE")
