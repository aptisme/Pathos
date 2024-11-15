import re
import os
import sys
import threading
import time

# Regex patterns for different platforms
patterns = {
    "WordPress": r'/wp-login\.php|wordpress/wp.login\.php|/wp-admin/user-new\.php|/wp-admin/install\.php|/wp-admin/options-writing\.php|/wp-admin/admin\.php|/wp-admin/post\.php|/wp-admin/options-general\.php',
    "Joomla": r'/administrator/index\.php',
    "Drupal": r'/user/login',
    "cPanel": r':2083|cpanel\.',
    "FTP": r'ftp://|:21/'
}

# ANSI code for blue color
BLUE = '\033[94m'
RESET = '\033[0m'

# Function for loading animation
def loading_animation():
    while loading:
        for char in "|/-\\":
            sys.stdout.write(f"\r{BLUE}Loading... {char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.1)

def sort_by_platform(data, patterns):
    global loading
    sorted_data = {platform: [] for platform in patterns}
    sorted_data['Others'] = []

    # Start loading animation thread
    loading = True
    t = threading.Thread(target=loading_animation)
    t.start()

    for entry in data:
        matched = False
        for platform, pattern in patterns.items():
            if re.search(pattern, entry):
                sorted_data[platform].append(entry)
                matched = True
                break
        if not matched:
            sorted_data['Others'].append(entry)
    
    # Stop loading animation
    loading = False
    t.join()
    sys.stdout.write(f"\r{BLUE}Done!{RESET}            \n")  # Clear loading animation with blue "Done!"

    return sorted_data

def save_to_files(combined_sorted_data):
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    for platform, entries in combined_sorted_data.items():
        file_name = f'output/{platform}.txt'
        with open(file_name, 'w') as file:
            for entry in entries:
                file.write(entry + '\n')

def process_files_in_directory():
    # Initialize combined results dictionary
    combined_sorted_data = {platform: [] for platform in patterns}
    combined_sorted_data['Others'] = []

    # Get all .txt files in the current directory
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.txt')]

    for file_name in files:
        print(f"Processing file: {file_name}")
        try:
            with open(file_name, 'r') as file:
                data = file.read().splitlines()
        except FileNotFoundError:
            print(f"File {file_name} not found.")
            continue

        # Sort data
        sorted_data = sort_by_platform(data, patterns)

        # Combine results
        for platform, entries in sorted_data.items():
            combined_sorted_data[platform].extend(entries)

    # Save combined results to files
    save_to_files(combined_sorted_data)

if __name__ == "__main__":
    process_files_in_directory()
