from reachy_mini import ReachyMini
from reachy_mini.utils import create_head_pose
from reachy_mini.motion.recorded_move import RecordedMoves
from reachy_mini.motion.move import Move

import csv
import sys
import time
from datetime import datetime


# Section 3 - expressive greeting
#
# Condition A: fast simple_nod (1.20 s)
# Condition B: slow simple_nod (2.40 s)
#
# Everything else is held constant.

CONDITIONS = {
    "A": 1.20,
    "B": 2.40,
}

HEAD_YAW = 15
HEAD_SWEEP_DURATION = 1.0
PAUSE = 0.5

DANCE_LIBRARY = "pollen-robotics/reachy-mini-dances-library"
NOD_MOVE = "simple_nod"
LOG_FILE = "greeting_trials.csv"


class TimeScaledMove(Move):
    """Play the same recorded trajectory over a different duration."""

    def __init__(self, original_move, target_duration):
        self.original_move = original_move
        self.target_duration = target_duration
        self.scale = target_duration / original_move.duration

    @property
    def duration(self):
        return self.target_duration

    @property
    def sound_path(self):
        return self.original_move.sound_path

    def evaluate(self, t):
        original_t = t / self.scale

        # Keep evaluation just inside the source trajectory's valid interval.
        if original_t >= self.original_move.duration:
            original_t = max(0.0, self.original_move.duration - 1e-6)

        return self.original_move.evaluate(original_t)


def stage(name):
    print(f"[STAGE] {name}", flush=True)


def save_log(condition, nod_duration, start_time, end_time, status, error=""):
    try:
        with open(LOG_FILE, "r"):
            exists = True
    except FileNotFoundError:
        exists = False

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)

        if not exists:
            writer.writerow(
                [
                    "condition",
                    "nod_duration_seconds",
                    "start_time",
                    "end_time",
                    "completion_status",
                    "error",
                ]
            )

        writer.writerow(
            [
                condition,
                nod_duration,
                start_time,
                end_time,
                status,
                error,
            ]
        )


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("  python headnod.py A")
        print("  python headnod.py B")
        return

    condition = sys.argv[1].upper()

    if condition not in CONDITIONS:
        print("Condition must be A or B.")
        return

    nod_duration = CONDITIONS[condition]
    start_time = datetime.now().isoformat()
    status = "failed"
    error_message = ""

    stage(f"CONDITION_{condition}")
    stage(f"NOD_DURATION={nod_duration}s")

    try:
        moves = RecordedMoves(DANCE_LIBRARY)
        original_nod = moves.get(NOD_MOVE)

        print(
            f"Original simple_nod duration: {original_nod.duration:.2f}s",
            flush=True,
        )

        scaled_nod = TimeScaledMove(
            original_nod,
            nod_duration,
        )

        with ReachyMini() as mini:
            mini.enable_motors()
            mini.wake_up()

            stage("NEUTRAL_START")
            mini.goto_target(
                head=create_head_pose(yaw=0, pitch=0, degrees=True),
                antennas=[0.0, 0.0],
                duration=1.0,
            )
            time.sleep(PAUSE)

            # Conversation-app-inspired sweep-look behavior.
            # Identical in both conditions.
            stage("LOOK_LEFT")
            mini.goto_target(
                head=create_head_pose(yaw=HEAD_YAW, pitch=0, degrees=True),
                duration=HEAD_SWEEP_DURATION,
            )
            time.sleep(PAUSE)

            stage("LOOK_RIGHT")
            mini.goto_target(
                head=create_head_pose(yaw=-HEAD_YAW, pitch=0, degrees=True),
                duration=HEAD_SWEEP_DURATION,
            )
            time.sleep(PAUSE)

            stage("LOOK_CENTER")
            mini.goto_target(
                head=create_head_pose(yaw=0, pitch=0, degrees=True),
                duration=HEAD_SWEEP_DURATION,
            )
            time.sleep(PAUSE)

            # Experimental manipulation: only nod duration changes.
            stage(f"SIMPLE_NOD_{nod_duration}s")
            mini.play_move(
                scaled_nod,
                initial_goto_duration=1.0,
            )
            time.sleep(PAUSE)

            stage("RETURN_NEUTRAL")
            mini.goto_target(
                head=create_head_pose(yaw=0, pitch=0, degrees=True),
                antennas=[0.0, 0.0],
                duration=1.0,
            )

            stage("DONE")
            status = "completed"

    except Exception as e:
        error_message = str(e)
        stage(f"ERROR: {error_message}")

    end_time = datetime.now().isoformat()

    save_log(
        condition,
        nod_duration,
        start_time,
        end_time,
        status,
        error_message,
    )


if __name__ == "__main__":
    main()
