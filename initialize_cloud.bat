@echo off
setlocal enabledelayedexpansion

:: Initialize variables
set "cloud_size=10GB"
set "cloud_partitioned=false"

:: Set initial partition size for cloud
set /p "input_size=Initial Partition Size For Cloud (Default: 10GB, INCLUDE 'GB'/'MB', Example: '10GB'): "
if not "!input_size!"=="" set "cloud_size=!input_size!"

:: Setup log handler path
set "current_dir=%cd%"
set "log_path=%current_dir%\log.txt"

:: Setup cloud configuration by calling the Python script
python -c "from Handler.cfgHandler import ConfigHandler; print(ConfigHandler.setupDefault('%cloud_size%'))" > temp.txt 2> error.txt
if %errorlevel% neq 0 (
    echo Error setting up cloud configuration:
    type error.txt
    del error.txt
    exit /b 1
)
set /p cloud_partitioned=<temp.txt
del temp.txt

if "%cloud_partitioned%"=="True" (
    set "partition_path=%current_dir%\partitions"
    echo Cloud Partitioned: %partition_path% : %cloud_size%
    
    :: Create user database by calling the Python script
    python -c "from Handler.DBHandler import UserDatabase; UD = UserDatabase('user_database.db'); UD.create_table()" 2> error.txt
    if %errorlevel% neq 0 (
        echo Error creating user database:
        type error.txt
        del error.txt
        exit /b 1
    )
    echo User/Partition Database Created
    
    :: Create test user
    set /p "test_user=Create Test User? (y/n): "
    set "test_user=!test_user:~0,1!"
    
    if /i "!test_user!"=="y" (
        :: Create a test user partition by calling the Python script
        python -c "from Handler.PartitionManager import PartitionManager; from Utilities.BytesConverter import BytesManager; partManager = PartitionManager(); byteManager = BytesManager(); partManager.createPartition(key='testUser', size_t=byteManager.Gigabytes(1))" 2> error.txt
        if %errorlevel% neq 0 (
            echo Error creating test user partition:
            type error.txt
            del error.txt
            exit /b 1
        )
        echo Created testUser; 1GB
    ) else (
        if /i "!test_user!"=="n" (
            echo Okay - Skipping Test User.
        ) else (
            echo Please input 'y' or 'n'.
        )
    )
) else (
    echo Failed to setup cloud configuration.
)

exit /b
