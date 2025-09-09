import os
import struct
import os.path
from typing import List
from dataclasses import dataclass
from Crypto.Cipher import AES
from io import BufferedReader, BytesIO


@dataclass(frozen=True)
class TrpHeader:
    version: int
    file_size: int
    entry_num: int
    entry_size: int
    dev_flag: bool
    digest: str
    key_index: int
    padding: bytes


@dataclass(frozen=True)
class TrpEntry:
    name: str
    start_pos: int
    length: int
    flag: int
    padding: bytes


# Represents a .TRP file, used to store trophies in the playstation systems
class Trophy:
    np_comm_id: str = None
    header: TrpHeader = None
    entries: List[TrpEntry] = []
    file_handler: BufferedReader | BytesIO
    trophy_key = "21F41A6BAD8A1D3ECA7AD586C101B7A9"

    # If from_bytes is provided it does have priority over the filename
    # And the current trophy will be loaded starting from bytes
    def __init__(self, np_comm_id, filename=None, from_bytes=None):
        if not filename and not from_bytes:
            raise Exception(
                "You must either provide a valid filename or using a bytes stream to initialize the class."
            )

        if not np_comm_id:
            raise Exception("You must provide a valid game comm_id")

        if from_bytes:
            self.file_handler = BytesIO(from_bytes)
        else:
            if not os.path.isfile(filename):
                raise Exception("file not found: " + filename)

            f = open(filename, "rb")
            self.file_handler = f

        self.np_comm_id = np_comm_id

        magic_header = self.file_handler.read(4)

        print(magic_header)

        if magic_header != bytes.fromhex("dca24d00"):
            raise Exception("invalid .trp file provided.")

        self._parse_file()

    # def __del__(self):
    #     self.file_handler.close()

    # TODO: improve error checking
    def _parse_file(self):
        self.file_handler.seek(4)

        header_fmt = ">IQIII20sI44s"
        header_size = struct.calcsize(header_fmt)
        header_data = self.file_handler.read(header_size)

        header_fields = struct.unpack(header_fmt, header_data)

        self.header = TrpHeader(*header_fields)

        entries_fmt = ">32sQQI12s"
        entries_size = struct.calcsize(entries_fmt)

        for _ in range(self.header.entry_num):
            entry_data = self.file_handler.read(entries_size)
            entry_fields = list(struct.unpack(entries_fmt, entry_data))

            if not len(entry_fields) == 5:
                raise Exception("invalid entry field found.")

            entry_fields[0] = entry_fields[0].rstrip(b"x\00").decode()
            self.entries.append(TrpEntry(*entry_fields))

    def extract_files(self, custom_path=None):
        if os.path.isdir(self.np_comm_id):
            raise Exception(f"folder {self.np_comm_id} already exists, aborting.")

        os.mkdir(f"{custom_path}/{self.np_comm_id}")

        for file in self.entries:
            self.file_handler.seek(file.start_pos)
            data = self.file_handler.read(file.length)

            output_path = f"{self.np_comm_id}/{file.name}"

            if custom_path:
                output_path = f"{custom_path}/{output_path}"

            with open(output_path, "wb") as output_file:
                output_file.write(data)

    def decrypt_esfm_file(self, filename, as_file=False):
        encoded_np_id = self.np_comm_id.encode("utf-8").ljust(16, b"\x00")

        esfm_file = open(filename, "rb")
        game_iv = esfm_file.read(16)
        encrypted_data = esfm_file.read()

        cipher = AES.new(
            bytes.fromhex(self.trophy_key),
            AES.MODE_CBC,
            bytes.fromhex("00000000000000000000000000000000"),
        )
        derived_key = cipher.encrypt(encoded_np_id)

        cipher = AES.new(derived_key, AES.MODE_CBC, game_iv)
        decrypted_data = cipher.decrypt(encrypted_data)

        if as_file:
            with open(f"{filename}.xml", "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)
            return

        return decrypted_data
