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

    def __update_progress(self, fd, file_size, data, update_callback):
        if update_callback:
            self.current_transfer_size += len(data)
            update_callback(self.current_transfer_size, file_size)
        fd.write(data)

    def get_trophy_for_comm_id(
        self, np_comm_id, update_callback: Callable[[int, int], None]
    ):
        trophy_path = f"{USER_PATH}/{np_comm_id}/TROPHY.TRP"

        fd = open(f"{np_comm_id}.TRP", "wb")
        file_size = self.ftp.size(trophy_path)

        print(trophy_path)

        try:
            self.ftp.retrbinary(
                f"RETR {trophy_path}",
                lambda data: self.__update_progress(
                    fd, file_size, data, update_callback
                ),
            )
            fd.close()
            self.ftp.quit()
            self.current_transfer_size = 0
        except Exception as e:
            fd.close()
            self.current_transfer_size = 0
            print("error while fetching: ", e)


# Usage example
# if __name__ == "__main__":
#     pbar = None

#     def callback(curr_len, total_len):
#         global pbar
#         if not pbar:
#             pbar = progressbar.ProgressBar(max_value=total_len)
#             pbar.start()
#         pbar.update(curr_len)

#     pf = PsFTP()
#     pf.get_trophy_for_comm_id("NPWR06221_00", callback)
