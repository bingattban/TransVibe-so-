# First-model native build: Whisper Tiny

The reference companion is https://github.com/bingattban/TransVibe-android-; no older native repository is involved.

Pinned whisper.cpp commit: `d1be6fde11ac6e0407606b4e42fe72d34add8037`. Build target: Android arm64-v8a API 26 with NDK 28.2.13676358. Test JNI/Kotlin symbols, source fingerprints, C++ compilation and ELF dependency closure before delivery.

The SO repository automatically merges only the same tested non-draft PR head. After a green main build it dispatches the artifact to Android if `TRANSVIBE_ANDROID_DISPATCH_TOKEN` exists. Android also requires a cross-repo read token `TRANSVIBE_SO_READ_TOKEN`; import is a PR which undergoes full signed Preview/Release testing before its own conditional automatic merge.

A failed job, wrong fingerprint, missing token, absent Android main source, missing signed APK or incompatible JNI must block progress. Do not bypass the gate.

Only `ggml-tiny.bin` is active. Continue to the next model only following a successful physical Code On The Go build, actual inference and the owner's evaluation and approval.
