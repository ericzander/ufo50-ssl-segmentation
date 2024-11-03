@echo off
REM Given a filename, generates a folder with the image and mask as an example

REM Check if a filename was provided
if "%~1"=="" (
    echo Please provide a filename as an argument.
    exit /b
)

REM Assign the filename to a variable
set "filename=%~1"

labelme_export_json "%filename%"
