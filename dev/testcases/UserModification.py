from Handler.PartitionManager import PartitionManager
from Utilities.BytesConverter import BytesManager

bytemanager = BytesManager()

partManager = PartitionManager()

partManager.modifyPartition("testUser", bytemanager.ByteDetection("500mb"), "SIZETO")