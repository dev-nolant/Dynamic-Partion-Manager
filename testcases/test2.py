from PM import PartitionManager
from BM import BytesManager

bytemanager = BytesManager()

partManager = PartitionManager()

partManager.modifyPartition("testUser", bytemanager.ByteDetection("1gb"), "SIZETO")