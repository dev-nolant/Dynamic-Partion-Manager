@echo off
setlocal enabledelayedexpansion

:: Default parameters
set "API=True"
set "a=True"

:: Parse command line arguments
for %%A in (%*) do (
    if "%%~A"=="-a=False" set "a=False"
    if "%%~A"=="--API=False" set "API=False"
)

:: Print parameters (for debugging purposes)
echo API=!API!
echo a=!a!

:: Navigate to the root directory
cd /d "%~dp0"

:: Check for partitions.cfg in the partitions directory
if not exist "partitions\partition.cfg" (
    echo Error: The server needs to be initialized first.
    set /p "init=Would you like to initialize the server? (y/n): "
    if /I "!init!"=="y" (
        call initialize_cloud.bat
        if %errorlevel% neq 0 (
            echo Initialization failed. Please check the initialization script.
            pause
            exit /b 1
        )
    ) else (
        echo Server initialization aborted.
        pause
        exit /b 1
    )
)

:: Start the API server if the parameter is set to True
if /I "!API!"=="True" (
    echo Starting API server...
    python -m API 2> error.log
    if %errorlevel% neq 0 (
        echo An error occurred while starting the API server. Please check error.log for details.
    )
) else (
    echo API server not started due to parameter --API=False
)

:: Other parameters can be handled here
:: For example:
if /I "!a!"=="True" (
    echo Parameter -a is True
) else (
    echo Parameter -a is False
)

pause
