import os
import subprocess

def find_usb_drive(drive_name):
    # List all block devices and their mount points
    result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT,LABEL'], stdout=subprocess.PIPE, text=True)
    drives = result.stdout.splitlines()

    for drive in drives:
        if drive_name in drive:
            columns = drive.split()
            mount_point = columns[1] if len(columns) > 1 else None
            if mount_point:
                return mount_point

    return None

def get_security_key(drive_mount_point):
    key_file_path = os.path.join(drive_mount_point, 'security_key.txt')
    if os.path.exists(key_file_path):
        with open(key_file_path, 'r') as key_file:
            return key_file.read().strip()
    else:
        return None

def store_security_key(drive_mount_point, security_key):
    key_file_path = os.path.join(drive_mount_point, 'security_key.txt')
    with open(key_file_path, 'w') as key_file:
        key_file.write(security_key)

def main():
    initial_drive_name = "MY_USB_DRIVE"  # Replace with your initial USB drive name
    security_key = "your_secure_key_here"  # Replace with your security key

    drive_mount_point = find_usb_drive(initial_drive_name)

    if drive_mount_point:
        print(f"Drive {initial_drive_name} found at {drive_mount_point}")
        key = get_security_key(drive_mount_point)
        if key:
            print(f"Security Key retrieved: {key}")
        else:
            print("Security Key not found on the drive.")
    else:
        print(f"Drive {initial_drive_name} not found.")
        user_drive_name = input("Please enter the name of your USB drive: ")
        drive_mount_point = find_usb_drive(user_drive_name)
        
        if drive_mount_point:
            print(f"Drive {user_drive_name} found at {drive_mount_point}")
            store_security_key(drive_mount_point, security_key)
            print(f"Security Key stored on the drive {user_drive_name}.")
        else:
            print(f"Drive {user_drive_name} not found.")
