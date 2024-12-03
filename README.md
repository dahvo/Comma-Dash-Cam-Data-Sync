
# Comma AI Dash cam Footage Sync Tool using SFTP

This Python script synchronizes dash cam footage between a [Comma](https://comma.ai/shop/comma-3x) and a local directory on a computer using SFTP. 

---
## Features

- **Efficient file syncing**: Only downloads new or modified files.
- **Accurate time keeping**:Maintains original timestamps to accurately reference when the driving took place.
- **Continuous Operation**: Automatically retries until a connection is established.
- **Easy ssh key handling**: Automatically uses the default ssh key that the user setup in order to access their comma 3.
---

## Requirements

- **Python**: Version 3.6 or higher
- **Dependencies**:
  - [Paramiko](https://pypi.org/project/paramiko/): For SSH and SFTP functionality

---

## Usage

### Setup

1. **Clone or Download the Repository**:
   Clone this repository to your local machine or download the script file directly.

2. **Set up an SSH Key**:
   Follow the instructions listed [here](https://docs.comma.ai/how-to/connect-to-comma/) to set up an SSH key for your Comma.

3. **Create a virtual environment**:
   Create a virtual environment to manage dependencies and isolate the project environment.

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
4. **Install dependencies using pip:**:
   ```bash
   pip install paramiko
   ```
5. **Modify Connection Details**:
   Update the connection details (`remote_host`, `remote_user`, `remote_path`, `local_path`) in the script to match your setup.

   Example configuration:
   ```python
   sync_files(
       remote_host="192.168.0.207",
       remote_user="comma",
       remote_path="/data/media/0/realdata/",
       local_path="H:\drives\"
   )
   ```

6. **Run the Script**:
   Execute the script using Python:
   ```bash
   python get_drives.py
   ```
