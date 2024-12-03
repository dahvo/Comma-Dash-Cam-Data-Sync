import os
import stat
from paramiko import SSHClient, AutoAddPolicy
import time


def sync_files(remote_host, remote_user, remote_path, local_path):
    """
    Sync files from a remote server to a local directory using SFTP.

    Args:
        remote_host (str): The IP or hostname of the remote server.
        remote_user (str): The username for SSH authentication.
        remote_path (str): The remote directory to sync.
        local_path (str): The local directory to sync files into.
    """
    # Ensure local path exists
    os.makedirs(local_path, exist_ok=True)

    # Connect to the remote server
    with SSHClient() as ssh:
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(remote_host, username=remote_user)

        with ssh.open_sftp() as sftp:
            print("SFTP connection established.")

            def download_file(remote_file, local_file, file_attr):
                """Download a file if it differs in size or modification time."""
                local_file_exists = os.path.exists(local_file)
                remote_size = file_attr.st_size
                remote_mtime = file_attr.st_mtime

                if local_file_exists:
                    local_size = os.path.getsize(local_file)
                    local_mtime = os.path.getmtime(local_file)

                    # Skip if size and modification time match
                    if local_size == remote_size and local_mtime == remote_mtime:
                        return False  # No download occurred

                # Download the file
                print(f"Downloading: {remote_file} -> {local_file}")
                sftp.get(remote_file, local_file)

                # Verify the file size after download
                if os.path.getsize(local_file) != remote_size:
                    raise IOError(f"File size mismatch for {local_file}")

                # Update local file's modification time
                os.utime(local_file, (file_attr.st_atime, file_attr.st_mtime))
                return True  # File was downloaded

            def download_recursive(remote_dir, local_dir):
                """Recursively download directories and files."""
                for file_attr in sftp.listdir_attr(remote_dir):
                    remote_file = f"{remote_dir}/{file_attr.filename}"
                    local_file = os.path.join(local_dir, file_attr.filename)

                    if stat.S_ISDIR(file_attr.st_mode):
                        # Create local directory if it doesn't exist
                        os.makedirs(local_file, exist_ok=True)
                        download_recursive(remote_file, local_file)
                    else:
                        try:
                            download_file(remote_file, local_file, file_attr)
                        except Exception as e:
                            print(f"Error downloading {remote_file}: {e}")

            # Start recursive download
            download_recursive(remote_path.rstrip('/'), local_path)

        print("SFTP connection closed.")



if __name__ == "__main__":
    while True:
        try:
            sync_files(
                remote_host="192.168.0.207",
                remote_user="comma",
                remote_path="/data/media/0/realdata/",
                local_path="H:\\drives\\"
            )
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 60 seconds...")
            time.sleep(60)
