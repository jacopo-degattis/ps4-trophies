import tomllib
from ftplib import FTP
import progressbar

from typing import Any, Callable

USER_PATH = "/user/trophy/conf"


class PsFTP:
    ftp: FTP
    config: dict[str, Any]
    current_transfer_size = 0

    def __init__(self):

        config_file = open("config.toml", "rb")
        self.config = tomllib.load(config_file)

        ftp_config = self.config.get("ftp")

        if not ftp_config.get("ip") or not ftp_config.get("port"):
            raise Exception("missing `ip` or `port` fields in ftp in config file.")

        print(f"{ftp_config.get("ip")}:{ftp_config.get('port')}")

        self.ftp = FTP()
        self.ftp.connect(ftp_config.get("ip"), ftp_config.get("port"))

        config_file.close()

    def __update_progress_file(self, fd, file_size, data, update_callback):
        if update_callback:
            self.current_transfer_size += len(data)
            update_callback(self.current_transfer_size, file_size)

        fd.write(data)

    def __update_progress_stream(self, buffer, file_size, data, update_callback):
        if update_callback:
            self.current_transfer_size += len(data)
            update_callback(self.current_transfer_size, file_size)

        buffer += data

    def get_trophy_for_comm_id(
        self, np_comm_id, update_callback: Callable[[int, int], None], to_file=None
    ):
        trophy_path = f"{USER_PATH}/{np_comm_id}/TROPHY.TRP"

        buffer = None
        if to_file:
            buffer = open(f"{np_comm_id}.TRP", "wb")
            callback = self.__update_progress_file
        else:
            buffer = bytearray()
            callback = self.__update_progress_stream

        # Get total file size
        file_size = self.ftp.size(trophy_path)

        try:
            self.ftp.retrbinary(
                f"RETR {trophy_path}",
                lambda data: callback(buffer, file_size, data, update_callback),
            )
            self.ftp.quit()
            self.current_transfer_size = 0

            if to_file:
                buffer.close()
            else:
                return buffer
        except Exception as e:
            if to_file:
                buffer.close()
            self.current_transfer_size = 0
            print("error while fetching: ", e)
