#!/usr/bin/env python3
"""Fail-closed source verification for Whisper AUTO transcription.

Pinned upstream behavior: params.detect_language=true means detect ONLY and
return success with no transcript segments. The language string "auto" already
activates autodetection. This gate prevents accidentally delivering a linked
ARM64 library whose only output is an auto-detected language.
"""
import argparse
from pathlib import Path
import re

def verify(jni: Path, upstream: Path | None = None) -> None:
    cpp = jni.read_text(encoding="utf-8")
    assert 'params.detect_language = true;' not in cpp, (
        "JNI uses detection-only mode; whisper_full returns zero segments"
    )
    branch = re.search(
        r'if\s*\(lang\s*==\s*"auto"\s*\|\|\s*lang\.empty\(\)\)\s*\{([^}]+)\}',
        cpp
    )
    assert branch, "Missing auto language path"
    assert 'params.language = "auto";' in branch.group(1)
    assert 'params.detect_language = false;' in branch.group(1)
    assert 'whisper_full(holder->ctx, params, samples, numSamples)' in cpp
    assert 'whisper_full_n_segments(holder->ctx)' in cpp
    if upstream is not None:
        src = upstream.read_text(encoding="utf-8")
        assert re.search(
            r'if\s*\(params\.detect_language\)\s*\{\s*return\s+0\s*;',
            src
        ), "Pinned whisper.cpp contract changed; re-audit before building"
    print("PASS: auto language detection continues into speech transcription")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--jni", type=Path, required=True)
    p.add_argument("--upstream", type=Path)
    args = p.parse_args()
    verify(args.jni, args.upstream)
