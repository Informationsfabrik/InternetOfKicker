#!/bin/bash

# Navigate to the directory where your git repository is located
cd /path/to/your/repo

# Run git pull to update the repository
git pull

# Check if the git pull was successful
if [ $? -eq 0 ]; then
    echo "Git pull successful. Activating virtual environment..."
    # Activate the virtual environment
    source venv/bin/activate

    # Check if the virtual environment activation was successful
    if [ $? -eq 0 ]; then
        echo "Virtual environment activated. Installing requirements..."
        # Install the requirements
        pip install -r requirements.txt

        # Check if the pip install was successful
        if [ $? -eq 0 ]; then
            echo "Requirements installed. Executing Python script..."
            # Execute the Python file
            python soundboard.py
        else
            echo "Failed to install requirements. Not executing Python script."
        fi

        # Deactivate the virtual environment
        deactivate
    else
        echo "Failed to activate virtual environment. Not executing Python script."
    fi
else
    echo "Git pull failed. Not executing Python script."
fi
