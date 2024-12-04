import os
import sys
import subprocess

def run_tests():
    # Get the absolute path to the virtual environment's Python
    venv_python = os.path.abspath(os.path.join('venv', 'Scripts', 'python.exe'))
    
    # Change to the backend directory
    os.chdir('smart_meal_planner_backend')
    
    # Run pytest with the virtual environment's Python
    try:
        result = subprocess.run(
            [venv_python, '-m', 'pytest', 'tests/test_ai.py', '-v'],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests()) 