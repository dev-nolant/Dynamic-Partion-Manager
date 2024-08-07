from Handler.cfgHandler import ConfigHandler
from Handler.DBHandler import  UserDatabase

from Handler.logHandler import loghandle

from Utilities.BytesConverter import BytesManager
import os

byteManager = BytesManager()

logHandler = loghandle()
logHandler.pathset(os.getcwd())

cloud_size = input("(Default: 10Gb) Initial Partition Size For Cloud: (INCLUDE 'GB'/'MB', Example: '10GB')") or "10GB"

cloud = ConfigHandler.setupDefault(cloud_size)

if cloud == True:
    path = os.getcwd()

    partition_path = path + "\\" + "partitions"
    
    print(f"Cloud Partitioned: {path} : {cloud_size}")
    
    UD = UserDatabase("user_database.db")
    UD.create_table()
    print("User/Partition Database Created")
    
    test_user = input("Create Test User? (y/n): ")
    test_user = test_user.lower()
    
    from Handler.PartitionManager import PartitionManager
    partManager = PartitionManager()
    match test_user:
        case "y":
            UID = {'key': 'testUser', 'size_t': byteManager.Gigabytes(1)}
            try:
                partManager.createPartition(**UID)
                print("Created testUser; 1GB")
            except Exception as e:
                logHandler.log(e)
                
        case "n":
            print("Okay - Skipping Test User.")
        case "_":
            print("Please input 'y' or 'n'.")
            
    
else:
    print(cloud)

