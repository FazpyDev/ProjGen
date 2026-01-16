@echo off
setlocal ENABLEDELAYEDEXPANSION

echo =====================================
echo ProjGen Installer
echo =====================================
echo.

REM ---- Resolve paths ----
set ROOT_DIR=%~dp0
set APP_DIR=%ROOT_DIR%app
set BUILD_APP=%ROOT_DIR%\run.py

REM ---- Sanity check ----
if not exist "%BUILD_APP%" (
    echo ERROR: app\app.py not found
    pause
    exit /b 1
)

REM ---- Check Python ----
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Install from https://www.python.org/
    pause
    exit /b 1
)

REM ---- Check PyInstaller ----
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo PyInstaller not found. Installing...
    python -m pip install --upgrade pyinstaller
)

REM ---- Build EXE ----
echo.
echo Building projgen.exe ...
echo.

python -m PyInstaller ^
    --onefile ^
    --name projgen ^
    --paths "%APP_DIR%" ^
    --hidden-import app.TemplateFunctions ^
    --hidden-import app.Utils ^
    --add-data "%APP_DIR%\TemplateOptions.json;app" ^
    --add-data "%APP_DIR%\templates;app/templates" ^
    "%BUILD_APP%"

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

REM ---- Install directory ----
set INSTALL_DIR=%USERPROFILE%\projgen
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

REM ---- Copy EXE ----
copy /Y "%ROOT_DIR%dist\projgen.exe" "%INSTALL_DIR%" >nul

REM ---- Add to PATH (user-level) ----
echo Adding ProjGen to PATH...
for /f "tokens=2*" %%A in ('reg query HKCU\Environment /v PATH 2^>nul') do set CURRENT_PATH=%%B

echo !CURRENT_PATH! | find /I "%INSTALL_DIR%" >nul
if errorlevel 1 (
    setx PATH "!CURRENT_PATH!;%INSTALL_DIR%" >nul
)

REM ---- Cleanup ----
rmdir /S /Q "%ROOT_DIR%build" >nul 2>&1
rmdir /S /Q "%ROOT_DIR%dist" >nul 2>&1
del "%ROOT_DIR%projgen.spec" >nul 2>&1

echo.
echo =====================================
echo Installation Completed Successfully
echo =====================================
