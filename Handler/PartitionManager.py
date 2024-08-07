import os
from datetime import datetime
from Utilities.BytesConverter import BytesManager
from Handler.cfgHandler import ConfigHandler
from Handler.DBHandler import UserDatabase
import binascii
import dotenv

dotenv.load_dotenv()

byteManager = BytesManager()


def generate_api_key():
    return binascii.hexlify(os.urandom(20)).decode()



class PartitionManager:
    def __init__(self):
        path = os.getcwd()
        self.partition_path = os.path.join(path, "partitions")
        os.makedirs(self.partition_path, exist_ok=True)

        self.user_db = UserDatabase("user_database.db")
        self.config_handler = ConfigHandler(self.partition_path)
        self.byte_manager = BytesManager()

        self.currDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.actions = self.config_handler.getActions()
        self.maxPartitions = self.config_handler.getMaxPartitions()
        self.PartitionsSize = self.config_handler.getPartitionsSize()

        self.os = os

    def createPartition(self, key: str, size_t: int, limitations=None):
        default_partition_path = os.path.join(
            self.partition_path, "default_partition")
        server_size = os.path.getsize(default_partition_path) if os.path.exists(
            default_partition_path) else 0
        try:
            max_size = byteManager.ByteDetection(self.PartitionsSize)
            files = len([name for name in os.listdir(self.partition_path) if os.path.isfile(
                os.path.join(self.partition_path, name))]) - 1

            total_size = 0

            for name in os.listdir(self.partition_path):
                file_path = os.path.join(self.partition_path, name)
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)

            if files < int(self.maxPartitions) and (total_size - server_size) <= max_size:
                user_partition_path = os.path.join(
                    self.partition_path, f'partition_{key}')
                with open(user_partition_path, "wb") as user_partition:
                    user_partition.seek(size_t)
                    user_partition.write(b"\0")

                self.os.stat(user_partition_path).st_size
                self.user_db.add_user(key, False, size_t,
                                      self.currDate, generate_api_key())

                with open(default_partition_path, "wb") as server_partition:
                    server_partition.seek(server_size - size_t)
                    server_partition.write(b"\0")

                return "Success"
            elif int(self.maxPartitions) == -1 and (total_size - server_size) <= max_size:
                user_partition_path = os.path.join(
                    self.partition_path, f'partition_{key}')
                with open(user_partition_path, "wb") as user_partition:
                    user_partition.seek(size_t)
                    user_partition.write(b"\0")

                self.os.stat(user_partition_path).st_size
                self.user_db.add_user(key, False, size_t,
                                      self.currDate, generate_api_key())

                with open(default_partition_path, "wb") as server_partition:
                    server_partition.seek(server_size - size_t)
                    server_partition.write(b"\0")

                return "Success"
            else:
                return "Operation Failed (Error: Partitions Overflow - Blocked)"
        except Exception as error:
            return f"Operation Failed (Error: {error})"

    def modifyPartition(self, key: str, value: int, mode: str):
        default_partition_path = os.path.join(
            self.partition_path, "default_partition")
        server_size = os.path.getsize(default_partition_path) if os.path.exists(
            default_partition_path) else 0

        mode = mode.upper()

        premium_max = self.byte_manager.ByteDetection(
            self.config_handler.getMaxPremium())
        default_max = self.byte_manager.ByteDetection(
            self.config_handler.getUserSize())

        if "SIZETO" in mode:
            if value <= default_max:
                user_partition_path = os.path.join(
                    self.partition_path, f'partition_{key}')
                user_size = os.path.getsize(user_partition_path)

                if value > user_size:
                    with open(default_partition_path, "wb") as server_partition:
                        server_partition.seek(
                            server_size - (value - user_size))
                        server_partition.write(b"\0")
                elif value < user_size:
                    with open(default_partition_path, "wb") as server_partition:
                        server_partition.seek(
                            server_size + (user_size - value))
                        server_partition.write(b"\0")

                with open(user_partition_path, "wb") as user_partition:
                    user_partition.seek(value)
                    user_partition.write(b"\0")

                self.user_db.update_allocated_space(key, value)
                return "Success"
            else:
                return f"Operation Failed (Error: User Partition Limit Hit - {default_max}. See config.)"

        elif "PREMIUM" in mode:
            user_partition_path = os.path.join(
                self.partition_path, f'partition_{key}')
            with open(user_partition_path, "wb") as user_partition:
                if value == 1:
                    self.user_db.update_premium_status(key, True, premium_max)
                    user_partition.seek(premium_max)
                    user_partition.write(b"\0")

                    with open(default_partition_path, "wb") as server_partition:
                        server_partition.seek(
                            (server_size + default_max) - premium_max)
                        server_partition.write(b"\0")

                    return "Success"
                elif value == 0:
                    self.user_db.update_premium_status(key, False, default_max)
                    user_partition.seek(default_max)
                    user_partition.write(b"\0")

                    with open(default_partition_path, "wb") as server_partition:
                        server_partition.seek(
                            (server_size + premium_max) - default_max)
                        server_partition.write(b"\0")

                    return "Success"
                else:
                    return "Operation Failed (Error: User Not Found or BOOLEAN not in range (0-1))"

    def getSize_t(self, key: str):
        return self.os.stat(os.path.join(self.partition_path, f'partition_{key}')).st_size


class PartitionFinder:
    def __init__(self, partition_path):
        self.partition_path = partition_path

    def create_file_hashmap(self):
        file_hashmap = {}
        for dirpath, dirnames, filenames in os.walk(self.partition_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                file_size = os.path.getsize(file_path)
                file_hashmap[filename] = file_size
        return file_hashmap

    def search_file_and_get_size(self, file_hashmap, file_name):
        if file_name in file_hashmap:
            return file_hashmap[file_name]
        else:
            return None  # File not found

    def searchPartitions(self, userKey):
        file_hashmap = self.create_file_hashmap()
        search_file_name = f"partition_{userKey}"
        file_size = self.search_file_and_get_size(
            file_hashmap, search_file_name)
        if file_size is not None:
            user = UserDatabase("user_database.db").get_user(userKey)
            return {
                'allocated_space': user['allocated_space'],
                'used_space': user['used_space']
            }
        else:
            return None
