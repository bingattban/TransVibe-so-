# TransVibe SO

**New public native library repository:** https://github.com/bingattban/TransVibe-so-

Source-of-truth companion project: [TransVibe-android-](https://github.com/bingattban/TransVibe-android-).

This repository builds the real Android `arm64-v8a` Whisper JNI library from an exact checked-out Android JNI source and a pinned official whisper.cpp commit, on GitHub's Ubuntu runners. It does **not** compile C++ in Code On The Go and does not use any older native-builder repository.

The first model stage is `ggml-tiny.bin`. The native build checks the JNI/Kotlin contract before compilation, and then validates ELF64 AArch64, JNI exports, 16KiB page alignment and SHA-256. GitHub Actions outputs `transvibe-whisper-arm64-api26`.

Only successful source-main builds may request that the Android repository **create a native import Pull Request**, after its owner sets the scoped GitHub Actions secret `TRANSVIBE_ANDROID_DISPATCH_TOKEN`. No automatic merging, no diagnostic stub passed off as a real model, and no model weights in the public repositories.

See [the first-stage runbook](README_FIRST_STAGE.md). 
