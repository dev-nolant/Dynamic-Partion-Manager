
# 📂 WORK IN PROGRESS. This is in Alpha, and is being updated regularly.

## Overview
I created this project to manage partitions locally within a folder. The idea is to help users reserve space for their personal servers with proper organization. Although the project is not fully complete and might not reach the intended use in the near future (as I've shifted my focus to Embedded Systems and Rust Development), it still offers a functional foundation for managing partitions.

## Project Goals
- Utilize only necessary imports, allowing for easy transfer and setup on any system.
- Developed and tested with Python 3.10.13.
- Open for contributions and feedback through pull requests and issues.

## Getting Started

### Installation
Clone the repository and navigate to the project directory:
```bash
git clone https://github.com/dev-nolant/partition-manager-dev.git
cd partition-manager-dev
```

Install Requirements
```bash
pip install -r requirements.txt
```

Update .env
1. Change env.example to .env. Replace CLIENT_ID and SECRET for GitHub with your GitHub client secret and ID.
2. Generate a secret key given the URL in the .env for your database.
3. OPTIONAL: Update if you want partitions/configs to be in the CWD and if you want a different database name. I recommend you leave than as is.
4. Run start.bat (windows) other distributions may come if popularity grows. And follow the steps. I recommend opening a CMD or Powershell window, and running the batch file via that window. Easier for debugging if anything goes wrong.

NOTE
* There is built-in logging, this can be disabled in api.py under (root)/API/api.py. Just change LOGGING_ENABLED=True to False. It is __ENABLED by default__.
* This project currently requires the GitHub API for OAuthorization. It's implemented in the system to allow admins and users to sign up.

TODO (No Specific Order)
- [x] There is currently a broken partition allocation section that causes recessive allocated space regardless of upload.
- [ ] There is no file deletion option.
- [ ] There currently is no ROLE system in-place, but that should be coming up momentarily. Currently, everyone is visitor role, and only has access to their own data.
- [ ] There will be an update with USER_ID systems being implemented for better file tracing and user handling.
- [ ] Moderation is expected to be added promptly after a ROLE system is implemented.


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
