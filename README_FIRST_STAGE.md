# TransVibe Native Builder — first accepted model only

This **new** public repository independently builds the production Android ARM64 `libtransvibe_whisper.so`, using the **exact JNI C++ file from the companion Android repository**. It does not reuse any former native builder repository.

Companion Android repository: https://github.com/bingattban/TransVibe-android-

Initial model gate: `ggml-tiny.bin`. No model weights are bundled; do not activate a second model before a real Code On The Go APK build, model inference validation and owner approval.

Build prerequisites: Ubuntu GitHub runner, Android SDK/NDK 28.2.13676358, CMake, Ninja; upstream whisper.cpp pinned at commit `d1be6fde11ac6e0407606b4e42fe72d34add8037` (v1.9.5). Output must be Android arm64-v8a API 26 with 16 KiB segment alignment; exported JNI methods and ELF dependencies are checked.

**Security gate**: native output is a workflow Artifact only. An optional cross-repository dispatch is sent after a successful build on `main` *when* the maintainer has installed the fine-grained `TRANSVIBE_ANDROID_DISPATCH_TOKEN` Actions secret, granting Actions write access **only** to TransVibe-android-. The Android workflow verifies the run and creates a Pull Request with the .so and manifest. There is no automatic merge.

A successful native compile does not establish on-device model quality or runtime success. The first model remains unapproved until full phone testing.
