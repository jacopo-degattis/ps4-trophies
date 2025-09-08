import io
import os
import struct
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

import utils


class SealedKey:
    magic: bytes
    key_set: bytes
    align_bytes: bytes
    iv: bytes
    encrypted_key: bytes
    sha256: bytes

    def __init__(self, magic, key_set, align_bytes, iv, encrypted_key, sha256):
        self.magic = magic
        self.key_set = key_set
        self.align_bytes = align_bytes
        self.iv = iv
        self.encrypted_key = encrypted_key
        self.sha256 = sha256

    @staticmethod
    def load_sealed_key(buff):
        stream = io.BytesIO(buff)

        magic_header = stream.read(8)
        key_set = stream.read(2)
        align_bytes = stream.read(6)
        iv = stream.read(16)
        encrypted_key = stream.read(32)
        sha256 = stream.read(32)

        if magic_header != b"pfsSKKey":
            print("Error: invalid sealed key provided.")
            exit(-1)

        return SealedKey(magic_header, key_set, align_bytes, iv, encrypted_key, sha256)


"""
    file_bytes: trophy file bytes
    sealed_key: sealed_key path
"""


def sealed_trophy(file_bytes, sealed_key):
    sealedkey_encrypted = open(sealed_key, "rb").read()
    sealed_key = SealedKey.load_sealed_key(sealedkey_encrypted)

    # Decrypted using the rev engineered `sce_sbl_ss_decrypt_sealed_key` func
    decrypted_key_reversed = bytearray(32)
    utils.sce_sbl_ss_decrypt_sealed_key(sealedkey_encrypted, decrypted_key_reversed)

    print("Your PFS Key is:", decrypted_key_reversed.hex())
    print("Your PFS IV is: ", sealed_key.iv.hex())

    # Decrypted using dumped PS4 internal keys
    cipher = AES.new(utils.KEYSET_KEYS.get(1), AES.MODE_CBC, sealed_key.iv)
    decrypted_trophy = cipher.decrypt(file_bytes)

    return decrypted_trophy


def parse_trp_file(filename):
    f = open(filename, "rb")
    trp_file_data = f.read()
    buff = io.BytesIO(trp_file_data)

    magic = buff.read(4)

    if magic != bytes.fromhex("dca24d00"):
        print("Error: invalid trp file")
        exit(-1)

    header_fmt = ">IQIII20sI44s"
    header_size = struct.calcsize(header_fmt)
    header_data = buff.read(header_size)

    version, file_size, entry_num, entry_size, dev_flag, digest, key_index, padding = (
        struct.unpack(">IQIII20sI44s", header_data)
    )

    trp_header = {
        "version": version,
        "file_size": file_size,
        "entry_num": entry_num,
        "entry_size": entry_size,
        "dev_flag": bool(dev_flag),
        "digest": digest.hex(),
        "key_index": key_index,
        "padding": padding.hex(),
    }

    print("== HEADER INFOS ==")
    print(trp_header)

    entries_fmt = ">32sQQI12s"
    entries_size = struct.calcsize(entries_fmt)

    trp_entries = []
    for x in range(trp_header.get("entry_num")):
        entries_data = buff.read(entries_size)
        name, pos, length, flag, padding = struct.unpack(entries_fmt, entries_data)
        trp_entries.append(
            {
                "name": name.rstrip(b"x\00").decode(),
                "start_pos": pos,
                "length": length,
                "flag": flag,
                "padding": padding.hex(),
            }
        )

    print("\n\n== ENTRY INFOS ==")
    print(trp_entries)

    # try to dump data

    # NPWR32931_00 hard-coded but npcommId should be derived automatically
    os.mkdir("NPWR32931_00")
    for entry in trp_entries:
        start = entry.get("start_pos")
        end = start + entry.get("length")
        data = trp_file_data[start:end]

        with open("NPWR32931_00/" + entry.get("name"), "wb") as output:
            output.write(data)


# def decrypt_esfm(esfm_file):
#     test_file = "NPWR32931_00/TROP.ESFM"

#     f = open(test_file, "rb")
#     data = f.read()

#     file_input = io.BytesIO(data)

#     game_iv = file_input.read(16)
#     encrypted_data = file_input.read()

#     trophy_key = bytes.fromhex("21F41A6BAD8A1D3ECA7AD586C101B7A9")
#     np_id = "NPWR32931_00".encode("utf-8").ljust(16, b"\x00")
#     keygen_iv = bytes.fromhex("c03f1df77ff0bbbc33b33efd488401ff")

#     cipher = AES.new(trophy_key, AES.MODE_CBC, keygen_iv)
#     derived_key = cipher.encrypt(np_id)

#     cipher = AES.new(derived_key, AES.MODE_CBC, game_iv)
#     decrypted_data = cipher.decrypt(encrypted_data)

#     with open("trop.esfm.xml", "wb") as out_xml:
#         out_xml.write(decrypted_data)


def decrypt_esfm():
    test_file = "NPWR32931_00/TROP.ESFM"

    with open(test_file, "rb") as f:
        file_input = io.BytesIO(f.read())

    game_iv = file_input.read(16)
    encrypted_data = file_input.read()

    trophy_key = bytes.fromhex("21F41A6BAD8A1D3ECA7AD586C101B7A9")

    np_id = "NPWR32931_00".encode("utf-8").ljust(16, b"\x00")

    cipher = AES.new(
        trophy_key, AES.MODE_CBC, iv=bytes.fromhex("00000000000000000000000000000000")
    )
    derived_key = cipher.encrypt(np_id)

    print("Derived key =", derived_key.hex())

    cipher = AES.new(derived_key, AES.MODE_CBC, iv=game_iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    with open("trop.esfm.xml", "wb") as out_xml:
        out_xml.write(decrypted_data)


# if __name__ == "__main__":
#     trophy_img = open("trophy.img", "rb").read()
#     dec_trophy = sealed_trophy(trophy_img, "sealedkey")

#     # dump decrypted trophy img
#     decrypted_trophy_out = open("testdecrypt.dat", "wb")
#     decrypted_trophy_out.write(dec_trophy)
#     decrypted_trophy_out.close()

if __name__ == "__main__":
    # parse_trp_file("TROPHY.TRP")
    decrypt_esfm()
