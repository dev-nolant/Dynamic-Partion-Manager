from PartitionManager import PartitionManager
from BytesConverter import BytesManager

bytemanager = BytesManager()

partManager = PartitionManager()

partManager.modifyPartition("testUser", bytemanager.ByteDetection("1gb"), "SIZETO")
