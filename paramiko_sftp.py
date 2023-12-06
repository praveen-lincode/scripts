# import paramiko

# def transfer_files(source_host, source_username, source_password, source_path, destination_host, destination_username, destination_password, destination_path):
#     # Connect to the source system
#     source_transport = paramiko.Transport((source_host, 22))
#     source_transport.connect(username=source_username, password=source_password)
#     source_sftp = source_transport.open_sftp()

#     # Connect to the destination system
#     destination_transport = paramiko.Transport((destination_host, 22))
#     destination_transport.connect(username=destination_username, password=destination_password)
#     destination_sftp = destination_transport.open_sftp()

#     try:
#         # Transfer the file
#         source_file = source_sftp.open(source_path, 'r')
#         destination_sftp.putfo(source_file, destination_path)
#         print('File transfer successful.')
#     except Exception as e:
#         print(f'Error occurred during file transfer: {str(e)}')
#     finally:
#         # Close the connections
#         source_sftp.close()
#         source_transport.close()
#         destination_sftp.close()
#         destination_transport.close()

# # Example usage
# source_host = '192.168.5.4'
# source_username = 'Praveen Peter'
# source_password = '123123123'
# source_path = 'D:\lincode\scripts\aa.txt'

# destination_host = '192.168.5.5'
# destination_username = 'sansera'
# destination_password = 'admin'
# destination_path = '/home/sansera/Documents/test/aa.txt'

# transfer_files(source_host, source_username, source_password, source_path, destination_host, destination_username, destination_password, destination_path)

# # Example usage
# local_file = "D:\lincode\scripts\aa.txt"
# remote_file = '/home/sansera'
# remote_hostname = '192.168.10.5'
# remote_username = 'sansera'
# remote_password = 'admin'

# sftp_transfer(local_file, remote_file, remote_hostname, remote_username, remote_password)

# ssh.connect("19.16.2.2", username="user1", password="pass", allow_agent=False)


# import pysftp

# def transfer_files(source_host, source_username, source_password, source_path, destination_host, destination_username, destination_password, destination_path):
#     # Connect to the source system
#     source_cnopts = pysftp.CnOpts()
#     source_cnopts.hostkeys = None  # Disable host key verification
#     with pysftp.Connection(host=source_host, username=source_username, password=source_password, cnopts=source_cnopts) as source_sftp:
#         # Connect to the destination system
#         destination_cnopts = pysftp.CnOpts()
#         destination_cnopts.hostkeys = None  # Disable host key verification
#         with pysftp.Connection(host=destination_host, username=destination_username, password=destination_password, cnopts=destination_cnopts) as destination_sftp:
#             try:
#                 # Transfer the file
#                 source_sftp.get(source_path)
#                 destination_sftp.put(source_path, destination_path)
#                 print('File transfer successful.')
#             except Exception as e:
#                 print(f'Error occurred during file transfer: {str(e)}')

# # Example usage
# # source_host = 'source.example.com'
# # source_username = 'source_username'
# # source_password = 'source_password'
# # source_path = '/path/to/source/file.txt'

# # destination_host = 'destination.example.com'
# # destination_username = 'destination_username'
# # destination_password = 'destination_password'
# # destination_path = '/path/to/destination/file.txt'


# # Example usage
# source_host = '192.168.5.4'
# source_username = 'Praveen Peter'
# source_password = '123123123'
# source_path = 'D:\lincode\scripts\aa.txt'

# destination_host = '192.168.5.5'
# destination_username = 'sansera'
# destination_password = 'admin'
# destination_path = '/home/sansera/Documents/test/aa.txt'

# transfer_files(source_host, source_username, source_password, source_path, destination_host, destination_username, destination_password, destination_path)


# *******************************************************


# import paramiko
# client  = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(hostname='192.168.5.5',username='sansera',password='admin',allow_agent=False,look_for_keys=False)

# sftp = client.open_sftp()
# sftp.put('aa.txt','abc.txt')
# sftp.close()


# ****************************

# import paramiko

# source_transport = paramiko.Transport(('192.168.5.5', 22))
# source_transport.connect(username='sansera', password='admin')
# source_sftp = source_transport.open_sftp()
# print("----------before--------------")
# source_file = source_sftp.open('D:\lincode\scripts\aa.txt', 'r')
# print("=------------after------------")

# client  = paramiko.SSHClient()
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# client.connect(hostname='192.168.5.5',username='sansera',password='admin',allow_agent=False,look_for_keys=False)

# sftp = client.open_sftp()
# sftp.putfo(source_file,'/home/abc.txt')
# sftp.close()

# **********************************

import paramiko


try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='192.168.1.5',username="jeba",password="1989",allow_agent=False,look_for_keys=False,port=22)
    sftp_client = ssh.open_sftp()
    print("\n-----------connected to the host ---------------")
except:
    print("\n------------Not Connected-------------")
    exit()
try:
    
    # print(dir(sftp_client))
    # sftp_client.chdir('/home/')
    # print(sftp_client.getcwd())
    # sftp_client.get('/home/sansera/sansera.txt','ssss.txt')   # getting data from the server to local
    sftp_client.put("D:\\lincode\\21 teeth\\21 teeth.zip","/home/vinayakaob/Documents/manju/abcd.zip") # sending the data local to the server
    print("\n---------file transfered---------")
except:
    print("\n--------some issue in file transfering----------")
finally:
    sftp_client.close()
    ssh.close()



# ***********************************


