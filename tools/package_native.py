#!/usr/bin/env python3
"""Validate and package a real Android AArch64 JNI ELF, fail closed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess

METHODS=("nativeIsLinked","nativeInit","nativeCancel","nativeTranscribe","nativeFree")
PREFIX="Java_com_transvibe_app_nativebridge_WhisperNativeBridge_"
ALLOWED_NEEDED={"libc.so","libm.so","libdl.so","liblog.so","libandroid.so"}

def sha(p:Path)->str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify_elf(path:Path, readelf:str):
    data=path.read_bytes()
    assert len(data)>65536, "Unexpectedly small JNI binary"
    assert data[:6]==b"\x7fELF\x02\x01", "Not a little-endian ELF64"
    assert struct.unpack_from("<H",data,16)[0]==3, "Not an ELF shared object"
    assert struct.unpack_from("<H",data,18)[0]==183, "Not AArch64"
    symbols=subprocess.check_output([readelf,"-Ws",str(path)],text=True)
    for name in METHODS:
        assert PREFIX+name in symbols, "Missing exported JNI function: "+name
    header=subprocess.check_output([readelf,"-lW",str(path)],text=True)
    aligns=[]
    for line in header.splitlines():
        if re.match(r"\s*LOAD\s+",line):
            last=line.split()[-1]
            aligns.append(int(last,16))
    assert aligns and all(x>=0x4000 for x in aligns), "LOAD segments are not 16KiB aligned"
    dynamic=subprocess.check_output([readelf,"-dW",str(path)],text=True)
    needed=set(re.findall(r"\(NEEDED\).*?\[([^]]+)\]",dynamic))
    assert needed <= ALLOWED_NEEDED, "Unbundled dynamic dependencies: "+repr(needed-ALLOWED_NEEDED)
    return sorted(needed)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--so",type=Path,required=True)
    ap.add_argument("--jni",type=Path,required=True)
    ap.add_argument("--whisper-sha",required=True)
    ap.add_argument("--app-commit",required=True)
    ap.add_argument("--readelf",required=True)
    ap.add_argument("--output",type=Path,required=True)
    a=ap.parse_args()
    assert re.fullmatch("[0-9a-f]{40}",a.whisper_sha)
    assert re.fullmatch("[0-9a-f]{40}",a.app_commit)
    needed=verify_elf(a.so,a.readelf)
    folder=a.output/"app/libs/arm64-v8a"
    folder.mkdir(parents=True,exist_ok=True)
    binary=folder/"libtransvibe_whisper.so"
    shutil.copyfile(a.so,binary)
    manifest={
        "schema_version":1,"engine":"whisper.cpp","first_model":"ggml-tiny.bin",
        "abi":"arm64-v8a","min_sdk":26,
        "app_repository":"bingattban/TransVibe-android-",
        "app_source_commit":a.app_commit,
        "jni_source_sha256":sha(a.jni),
        "whisper_commit":a.whisper_sha,
        "binary_sha256":sha(binary),"needed":needed,
        "verification":"ELF-ABI-JNI-link-only; physical device inference NOT verified",
        "builder_repository":"bingattban/TransVibe-so-",
        "builder_run_id":os.environ.get("GITHUB_RUN_ID","local")
    }
    (a.output/"native-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print("PASS: Android ARM64 native package:",binary,manifest["binary_sha256"])

if __name__=="__main__": main()
