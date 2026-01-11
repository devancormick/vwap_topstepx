"""Helper script to copy strategy files to backend for Docker builds."""

import shutil
import os

def copy_strategy_files():
    """Copy vwap_strategy.py and config.py to backend directory."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    strategy_file = os.path.join(project_root, 'vwap_strategy.py')
    config_file = os.path.join(project_root, 'config.py')
    
    if os.path.exists(strategy_file):
        shutil.copy(strategy_file, backend_dir)
        print(f"Copied {strategy_file} to {backend_dir}")
    
    if os.path.exists(config_file):
        shutil.copy(config_file, backend_dir)
        print(f"Copied {config_file} to {backend_dir}")

if __name__ == "__main__":
    copy_strategy_files()

