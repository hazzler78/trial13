@echo off
cd smart_meal_planner_backend
call ..\venv\Scripts\activate.bat
python -m pytest tests\test_ai.py -v
pause 