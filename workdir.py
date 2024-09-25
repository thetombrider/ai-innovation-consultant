import os

# Assuming your project directory is one level up from the venv directory
project_dir = '/Users/tommy/Progetti Python/ai-innovation-consultant/'
os.chdir(project_dir)

# Print the new working directory to confirm
print(f"Current working directory: {os.getcwd()}")