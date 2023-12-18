import ssl
import socket
import cv2, struct, pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

HOST='localhost'
PORT=6631

# Key, must be same for both server and client
ENCRYPTIONKEY = b'1234567890123456'

def decrypt_pickle(encrypted_data, key):
    # Extract the IV from the encrypted data
    iv = encrypted_data[:16]
    
    # Extract the ciphertext from the encrypted data
    ciphertext = encrypted_data[16:]

    # Decrypt the ciphertext
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()

    # Use PKCS7 unpadding
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()

    # Deserialize the object using pickle.loads()
    obj = pickle.loads(unpadded_data)
    return obj

if __name__ == "__main__":
    # Create client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # connect to server_socket
    client_socket.connect((HOST, PORT))

    data = b""
    payload_size = struct.calcsize("Q")

    # send video stream
    while True:
        # get video frame
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        # get video stream
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = decrypt_pickle(frame_data, ENCRYPTIONKEY)
        cv2.imshow("RECEIVING VIDEO FROM SERVER",frame)
        key = cv2.waitKey(1) & 0xFF

        # press `q` to exit
        if key  == ord('q'):
            break
    client_socket.close()