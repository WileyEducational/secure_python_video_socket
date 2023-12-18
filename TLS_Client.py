import ssl
import socket
import cv2, struct, pickle

HOST='localhost'
PORT=6636

if __name__ == "__main__":
    # Create a context, just like as for the server
    context = ssl.create_default_context()
    # Load the server's CA
    context.load_verify_locations('./keys/localhost.crt')
    
    # Wrap the socket, just as like in the server.
    client_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname="localhost")
    
    # Connect to server_socket
    client_socket.connect((HOST, PORT))
    print("CONNECTED TO: ",(HOST, PORT))

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
        frame = pickle.loads(frame_data)
        cv2.imshow("RECEIVING VIDEO FROM SERVER",frame)
        key = cv2.waitKey(1) & 0xFF

        # press `q` to exit
        if key  == ord('q'):
            break
    client_socket.close()