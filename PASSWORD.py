import hashlib
import platform
import getpass
import uuid
'''
def get_full_path(filename):
    try:
        if getattr(sys, 'frozen', False):
            current_directory = os.path.dirname(sys.executable)
        else:
            current_directory = os.path.dirname(os.path.abspath(__file__))
        
        file_path = os.path.join(current_directory, filename)
        return file_path
    except Exception as e:
        print(f'Error getting full path: {e}')

'''

def get_device_ID():
    windows_uuid = None
    if platform.system() == 'Windows':
        deviceID = str(uuid.UUID(int=uuid.getnode()))
       # print(deviceID)
    return deviceID

def get_device_identifier():
    identifier = platform.node()  + get_device_ID() + getpass.getuser()
    #print(identifier)
    return identifier

def generate_lock(device_identifier):
    secretkey = 'ASALE LAMASAB'
    # print(hashlib.sha256((device_identifier+secretkey).encode()).hexdigest())
    return hashlib.sha256((device_identifier + secretkey).encode()).hexdigest()

device_identifier = get_device_identifier()
PASSWORD_ENTRY = generate_lock(device_identifier)
'''
print(PASSWORD_ENTRY)
'''
# Write variables to password.txt file
'''with open('password.txt', 'w') as file:
    #file.write(f"Device Identifier: {device_identifier}\n")
    file.write(f"{PASSWORD_ENTRY}")
'''