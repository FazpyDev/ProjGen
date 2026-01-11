@echo off
REM Build the wheel
python -m build

REM Install with pipx, fallback to user pip install
pipx install --force dist\FlaskProject-1.0.0-py3-none-any.whl || pip install --user dist\FlaskProject-1.0.0-py3-none-any.whl

echo Installation complete! You can now run "FlaskProject" from any command prompt.
pause