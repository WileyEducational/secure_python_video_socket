import ssl
import socket
import cv2, struct, pickle
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from os import urandom

HOST='localhost'
PORT=6639

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
    # First, create a context. The default settings are probably the best here. 
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    
    # Load the CA (self-signed, in this case) and the corresponding private key (also self-signed, in this case)
    context.load_cert_chain(certfile="./keys/localhost.crt", keyfile="./keys/localhost.key")

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
            conn, addr = server_socket.accept()

            # wrap the standard socket with the SSLContext, now it is a secure connection
            with context.wrap_socket(conn, server_side=True) as secure_conn:
                print('GOT CONNECTION FROM:',addr)

                # if client socket is true
                if secure_conn:
                    # make data stream
                    vid = cv2.VideoCapture(0)
                    
                    # send video stream
                    while(vid.isOpened()):
                        img,frame = vid.read()
                        a = encrypt_pickle(frame, ENCRYPTIONKEY)
                        message = struct.pack("Q",len(a))+a
                        secure_conn.sendall(message)
                        
                        cv2.imshow('TRANSMITTING VIDEO TO CLIENT',frame)
                        key = cv2.waitKey(1) & 0xFF

                        # press `q` to exit
                        if key ==ord('q'):
                            secure_conn.close()
    except socket.timeout:
        pass

    server_socket.close()