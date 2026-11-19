# TransVibe SO

Public native builder: https://github.com/bingattban/TransVibe-so-
Companion application: https://github.com/bingattban/TransVibe-android-

This new repository compiles real CPU-only Whisper JNI for Android arm64-v8a/API 26 using a pinned official whisper.cpp commit and exact JNI/Kotlin contracts from the Android repository. It never reuses an older native-builder repository.

## Mandatory gates

1. Source contract and JNI/Kotlin tests run first.
2. Only if all pass, cross-compile ARM64 with Android NDK 28.2 on Ubuntu GitHub Actions.
3. Verify ELF64 AArch64, JNI exports, dynamic library dependencies, 16 KiB alignment, source identity and SHA-256. Upload the authenticated native artifact.
4. Automatically squash-merge an internal, ready pull request to main ONLY after successful tests/build and unchanged head SHA. Respect normal branch protections; never force merge.
5. On a successful main build, request a verified import PR in Android using the scoped `TRANSVIBE_ANDROID_DISPATCH_TOKEN`. Android CI automatically merges its import PR only after full source, native, JVM, signing, Preview and Release gates pass.

The first-model gate remains `ggml-tiny.bin`, pending owner acceptance of actual inference on the phone. No models or private keys are bundled. A successfully linked JNI binary does NOT prove ASR quality on-device.
