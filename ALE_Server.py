import ssl
import socket
import cv2, struct, pickle
from os import urandom
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


HOST='localhost'
PORT=6631

# Key, must be same for both server and client
ENCRYPTIONKEY = b'1234567890123456'

def encrypt_pickle(obj, key):
    # Serialize the object using pickle.dumps()
    serialized_obj = pickle.dumps(obj)

    # Generate a random IV (Initialization Vector)
    iv = urandom(16)

    # Use PKCS7 padding
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(serialized_obj) + padder.finalize()

    # Encrypt the padded data
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return the IV and the encrypted data
    return iv + ciphertext


if __name__ == "__main__":
    # Create a standard TCP socket, bind it to an address, and listen for connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to an address and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()
    print("Listening on port %d for incoming connections..." % PORT)

    # Start accepting incoming connections
    accepting = True 
    try:
        while accepting:
            # conn is a standard python socket, addr is where it originated
            client_socket, addr = server_socket.accept()

            print('GOT CONNECTION FROM:',addr)

            # if client socket is true
            if client_socket:
                # make data stream
                vid = cv2.VideoCapture(0)
                    
                # send video stream
                while(vid.isOpened()):
                    img,frame = vid.read()
                    a = encrypt_pickle(frame, ENCRYPTIONKEY)
                    message = struct.pack("Q",len(a))+a
                    client_socket.sendall(message)
                        
                    cv2.imshow('TRANSMITTING VIDEO TO CLIENT',frame)
                    key = cv2.waitKey(1) & 0xFF

                    # press `q` to exit
                    if key ==ord('q'):
                        client_socket.close()
    except socket.timeout:
        pass

    server_socket.close()