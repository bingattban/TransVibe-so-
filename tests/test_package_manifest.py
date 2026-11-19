"""Fail-closed native package regression checks; run before compiling Whisper."""
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from tools.package_native import verify_elf


class NativePackageManifestTests(unittest.TestCase):
    def test_rejects_too_short_binary(self):
        with TemporaryDirectory() as temp:
            file = Path(temp) / 'empty.so'
            file.write_bytes(b'\x7fELF\x02\x01')
            with self.assertRaisesRegex(AssertionError, 'small'):
                verify_elf(file, 'readelf')

    def test_rejects_wrong_elf_architecture_before_readelf(self):
        with TemporaryDirectory() as temp:
            data = bytearray(70000)
            data[0:6] = b'\x7fELF\x02\x01'
            data[16:18] = (3).to_bytes(2, 'little')
            data[18:20] = (62).to_bytes(2, 'little')
            file = Path(temp) / 'x86_64.so'
            file.write_bytes(data)
            with self.assertRaisesRegex(AssertionError, 'AArch64'):
                verify_elf(file, 'readelf')

    def test_requires_kotlin_hash_in_versioned_native_manifest(self):
        source = (Path(__file__).resolve().parents[1] / 'tools/package_native.py').read_text()
        self.assertIn('"schema_version":2', source)
        self.assertIn('"kotlin_source_sha256":sha(a.kotlin)', source)
        self.assertIn('ap.add_argument("--kotlin"', source)


if __name__ == '__main__':
    unittest.main()
