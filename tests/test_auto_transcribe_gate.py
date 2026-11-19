"""Tests-first gate for the documented Whisper detection-only API trap.

Pinned whisper.cpp returns zero transcript segments when detect_language=true.
The SO builder must use the NEW JNI source branch until Android main receives
the recompiled binary, then revert automatically to main.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class AutoTranscribeGate(unittest.TestCase):
    def test_native_builder_selects_fixed_app_branch_only_until_main_is_fixed(self):
        workflow = (ROOT / ".github/workflows/build-whisper-arm64.yml").read_text()
        self.assertIn("fix/whisper-auto-transcribe", workflow)
        self.assertIn("app_ref == 'fix/whisper-auto-transcribe'", workflow)
        self.assertIn("android-main/app/src/main/cpp/whisper_jni.cpp", workflow)

    def test_safety_check_excludes_detection_only_mode(self):
        source = (ROOT / "tools/check_transcription_mode.py").read_text()
        self.assertIn('params.detect_language = false;', source)
        self.assertIn('params.detect_language = true;', source)
        self.assertIn("whisper_full", source)

    def test_pinned_native_compiler_requires_real_transcription_contract(self):
        workflow = (ROOT / ".github/workflows/build-whisper-arm64.yml").read_text()
        self.assertIn("tools/check_transcription_mode.py", workflow)
        self.assertIn("whisper-source/src/whisper.cpp", workflow)

if __name__ == "__main__":
    unittest.main()
