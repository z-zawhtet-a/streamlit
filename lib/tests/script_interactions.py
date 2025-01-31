# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import os
import pathlib
import tempfile
import textwrap
import unittest
from unittest.mock import MagicMock

from streamlit.runtime import Runtime
from streamlit.runtime.media_file_manager import MediaFileManager
from streamlit.runtime.memory_media_file_storage import MemoryMediaFileStorage
from streamlit.testing.local_script_runner import LocalScriptRunner


class InteractiveScriptTests(unittest.TestCase):
    script_dir: tempfile.TemporaryDirectory

    def setUp(self) -> None:
        super().setUp()
        self.script_dir = tempfile.TemporaryDirectory()
        mock_runtime = MagicMock(spec=Runtime)
        mock_runtime.media_file_mgr = MediaFileManager(
            MemoryMediaFileStorage("/mock/media")
        )
        Runtime._instance = mock_runtime

    def tearDown(self) -> None:
        super().tearDown()
        Runtime._instance = None

    def script_from_string(self, script_name: str, script: str) -> LocalScriptRunner:
        """Create a runner for a script with the contents from a string.

        Useful for testing short scripts that fit comfortably as an inline
        string in the test itself, without having to create a separate file
        for it.
        """
        path = pathlib.Path(self.script_dir.name, script_name)
        aligned_script = textwrap.dedent(script)
        path.write_text(aligned_script)
        return LocalScriptRunner(str(path))

    def script_from_filename(self, script_name: str) -> LocalScriptRunner:
        """Create a runner for the script with the given name, for testing."""
        script_path = os.path.join(
            os.path.dirname(__file__), "streamlit", "test_data", script_name
        )
        return LocalScriptRunner(script_path)
