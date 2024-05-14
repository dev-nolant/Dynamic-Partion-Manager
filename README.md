# partition-manager-dev
A simple partition generator and manager with setup script and log handler.


# This is an experiment.
I wanted to work with handmade partitions that would work locally within a folder, so users could reserve space for their personal servers.
It isn't completed to intended use (yet), and isn't promised to be in the near future, as I've moved onto Embedded Systems and Rust Development.

This project was created to use very little to no external imports (PIP required imports). So users could easily transfer onto their system and run from factory.
This project was developed in 3.10.13.

I will respond to pull requests and issues!

Feel free to contribute, you will be listed as a contributor.

# Example Usage
```python
from PartitionManager import PartitionManager
from BytesConverter import BytesManager

bytemanager = BytesManager()

partManager = PartitionManager()

partManager.modifyPartition("testUser", bytemanager.ByteDetection("1gb"), "SIZETO")
```

