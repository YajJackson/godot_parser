import os
from typing import Any

from beartype import beartype
from pyparsing import inspect


@beartype
class SnapshotManager:
    def __init__(self, snapshot_directory="snapshots"):
        this_file = os.path.abspath(__file__)
        stack = inspect.stack()

        caller_frame = None
        for frame_info in stack:
            if frame_info.filename == this_file:
                continue

            file_name = os.path.basename(frame_info.filename)
            is_test_class = frame_info.function.startswith("Test")
            is_test_file = file_name.startswith("test_")
            if is_test_class and is_test_file:
                caller_frame = frame_info
                break

        if not caller_frame:
            raise Exception("SnapshotManager must be instantiated within a test class!")

        base_path = os.path.dirname(os.path.abspath(caller_frame.filename))
        test_file_name = os.path.splitext(os.path.basename(caller_frame.filename))[0]

        self.caller_class_name = caller_frame.function
        self.snapshot_directory = os.path.join(
            base_path, snapshot_directory, test_file_name
        )

        if not os.path.exists(self.snapshot_directory):
            os.makedirs(self.snapshot_directory)

    def _get_snapshot_path(self, snapshot_name):
        snapshot_file_name = f"{self.caller_class_name}.{snapshot_name}.snap"
        return os.path.join(self.snapshot_directory, snapshot_file_name)

    def assert_match(self, value: Any, snapshot_name: str):
        snapshot_path = self._get_snapshot_path(snapshot_name)
        if not os.path.exists(snapshot_path):
            with open(snapshot_path, "w") as f:
                f.write(value)

        with open(snapshot_path, "r") as f:
            expected_value = f.read()

        assert value == expected_value, f"Snapshot {snapshot_name} does not match!"
