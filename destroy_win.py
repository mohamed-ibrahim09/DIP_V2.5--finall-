import os
import sys
import subprocess

def destroy_and_restart(root):
    """
    Destroys the given Tkinter root window and restarts the script.
    Usage: destroy_and_restart(root)
    """
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "image_processor.py")
    root.destroy()
    try:
        # Try using 'python' command
        subprocess.Popen(['python', script_path])
    except FileNotFoundError:
        try:
            # Try using 'python3' command
            subprocess.Popen(['python3', script_path])
        except FileNotFoundError:
            try:
                # Try using sys.executable as last resort
                subprocess.Popen([sys.executable, script_path])
            except Exception as e:
                print(f"Failed to restart the application: {e}")
    sys.exit(0) 