
# 📂 WORK IN PROGRESS. This is in Alpha, and is being updated regularly.

## Overview
I created this project to manage partitions locally within a folder. The idea is to help users reserve space for their personal servers with proper organization. Although the project is not fully complete and might not reach the intended use in the near future (as I've shifted my focus to Embedded Systems and Rust Development), it still offers a functional foundation for managing partitions.

## Project Goals
- Utilize minimal to no external imports (no PIP required imports), allowing for easy transfer and setup on any system.
- Developed and tested with Python 3.10.13.
- Open for contributions and feedback through pull requests and issues.

## Getting Started

### Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/dev-nolant/partition-manager-dev.git
cd partition-manager-dev
```

### Usage Example
Here's a simple example to demonstrate how to use the `PartitionManager` and `BytesManager` classes:

```python
from PartitionManager import PartitionManager
from BytesConverter import BytesManager

# Initialize managers
bytemanager = BytesManager()
partManager = PartitionManager()

# Modify a partition
partManager.modifyPartition("testUser", bytemanager.ByteDetection("1gb"), "SIZETO")
```

### External Usage
If you plan to implement this project into your program, please add a comment noting the contribution and create an "Issue" with a link to your code. I'd love to see the cool implementations you create!

## Contributing
Contributions are welcome! Feel free to fork the repository, make changes, and submit a pull request. You will be listed as a contributor.

## Contact
I will respond to pull requests and issues. Don't hesitate to reach out with any questions or feedback.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
