@echo off
setlocal
cd /d "%~dp0"

if not exist "NOTES.md" (
  echo ERROR: NOTES.md was not found.
  echo Put this script and .gitignore inside your existing IssueInsight folder.
  exit /b 1
)

where py >nul 2>nul
if %errorlevel% equ 0 (
  echo Creating virtual environment with the Python launcher...
  py -m venv .venv
) else (
  echo Python launcher not found. Trying python...
  python -m venv .venv
)
if errorlevel 1 (
  echo ERROR: Could not create the virtual environment.
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Virtual environment Python not found.
  exit /b 1
)

echo.
echo Virtual environment created successfully.
".venv\Scripts\python.exe" -c "import sys; print('Using Python:', sys.executable); print('Environment:', sys.prefix)"
if errorlevel 1 exit /b 1

findstr /C:"Step 2: Created" "NOTES.md" >nul 2>nul
if errorlevel 1 (
  echo.>>NOTES.md
  echo - Step 2: Created a Python virtual environment to isolate project dependencies and configured Git to ignore local files.>>NOTES.md
)

echo.
echo Step 2 complete. Now verify the .venv folder and commit files using Git.
endlocal
