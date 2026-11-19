#!/usr/bin/env python3
"""Source-level ABI contract gate; not a device inference test."""
import argparse
from pathlib import Path
import re
import sys

METHODS = ("nativeIsLinked", "nativeInit", "nativeCancel", "nativeTranscribe", "nativeFree")
JNI_PREFIX = "Java_com_transvibe_app_nativebridge_WhisperNativeBridge_"

def check(cpp: str, kotlin: str):
    for method in METHODS:
        assert JNI_PREFIX + method in cpp, "Missing JNI symbol: " + method
        assert re.search(r"external\s+fun\s+" + method + r"\s*\(", kotlin), (
            "Missing Kotlin declaration: " + method
        )
    assert "TRANSVIBE_HAS_WHISPER_CPP=1" not in cpp, "Avoid fake inline JNI implementation"
    assert "#include \"whisper.h\"" in cpp
    assert "whisper_full(" in cpp
    assert "params.translate = false" in cpp, "ASR must not silently switch to translation"
    assert "numSamples > env->GetArrayLength(pcmData)" in cpp, "PCM buffer bounds guard missing"
    assert 'System.loadLibrary("transvibe_whisper")' in kotlin
    assert "nativeIsLinked()" in kotlin
    assert "Array<NativeWhisperSegment>" in kotlin

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cpp",type=Path)
    ap.add_argument("kotlin",type=Path)
    a=ap.parse_args()
    check(a.cpp.read_text(encoding="utf-8"), a.kotlin.read_text(encoding="utf-8"))
    print("PASS: exact Android JNI source/Kotlin ABI contract")

if __name__ == "__main__":
    try: main()
    except (AssertionError, OSError) as exc:
        print("FAIL:", exc, file=sys.stderr); sys.exit(1)
