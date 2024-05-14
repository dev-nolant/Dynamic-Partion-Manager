# This is an experiment.
I wanted to work with handmade partitions that would work locally within a folder, so users could reserve space for their personal servers with organization.
It isn't completed to intended use (yet), and isn't promised to be in the near future, as I've moved onto Embedded Systems and Rust Development.

This project was created to use very little to no external imports (PIP required imports). So users could easily transfer onto their system and run from factory.
This project was developed in ```3.10.13```.

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

# External Usage

If you plan to implement this into your program, all I ask is for a comment with a note of contribution in your code at the top or near the implementation and for you to make an "Issue" with a link to your code! I want to see the cool implementations you can create.
