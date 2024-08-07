from Handler.PartitionManager import PartitionManager, PartitionFinder
from Utilities.BytesConverter import BytesManager

partManager = PartitionManager()

partUtils = PartitionFinder()

byteManager = BytesManager()


UID = {'key': 'spaceKey', 'size_t': byteManager.Gigabytes(1)}
UID2 = {'key': 'spaceKey2', 'size_t': byteManager.Gigabytes(1)}

#print(partManager.createPartition(**UID))

#value = partManager.modifyPartition(UID["key"], value=byteManager.ByteDetection("1GB"), mode="SIZETO")
#value = partManager.modifyPartition(UID["key"], value=0, mode="PREMIUM")
#print(value)
#print(partUtils.searchPartitions(UID["key"]))

#partManager.modifyPartition(key=UID2['key'], size_t=UID['size_t'], value=(byteManager.Gigabytes(1)), mode="SIZETO")


