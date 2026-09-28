from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose

# Section 2 - modified Hello World
# Original antenna motion + one added head-motion behavior.

with ReachyMini() as mini:
    mini.enable_motors()
    mini.wake_up()

    print("[STAGE] START", flush=True)

    print("[STAGE] ANTENNAS_FIRST_POSITION", flush=True)
    mini.goto_target(
        antennas=[0.3, -0.3],
        duration=1.0,
    )

    print("[STAGE] ANTENNAS_REVERSE", flush=True)
    mini.goto_target(
        antennas=[-0.3, 0.3],
        duration=1.0,
    )

    print("[STAGE] HEAD_LEFT", flush=True)
    mini.goto_target(
        head=create_head_pose(yaw=8, pitch=0, degrees=True),
        duration=1.0,
    )

    print("[STAGE] HEAD_RIGHT", flush=True)
    mini.goto_target(
        head=create_head_pose(yaw=-8, pitch=0, degrees=True),
        duration=1.0,
    )

    print("[STAGE] RETURN_NEUTRAL", flush=True)
    mini.goto_target(
        head=create_head_pose(yaw=0, pitch=0, degrees=True),
        antennas=[0.0, 0.0],
        duration=1.0,
    )

    print("[STAGE] DONE", flush=True)
