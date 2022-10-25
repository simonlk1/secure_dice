import rsa
import socket
import ssl
from shared import BOB_PORT, HOST, PORT, agree_on_roll, generate_dice_roll

with open('bob.public.pem', mode='rb') as bobpublicfile:
    keydata = bobpublicfile.read()

bobpub = rsa.PublicKey.load_pkcs1(keydata)

with open('alice.private.pem', mode='rb') as aliceprivatefile:
    keydata = aliceprivatefile.read()

alicepriv = rsa.PrivateKey.load_pkcs1(keydata)

def serve():
    host = HOST
    port = PORT

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.vertify_mode = ssl.CERT_REQUIRED

    server = socket()
    server.bind((host, port)) 
    server.listen()

    tls = context.wrap_socket(server, server_side=True)
    connection, address = tls.accept()

    peerCertification = connection.getpeercert()
    print(f"Certificate obtained from the Bob? {peerCertification != None}")

    hShake = connection.do_handshake()
    print(f"Handshake done: {hShake == None}")

    a, b, c = connection.cipher()
    print('TLS cipher: ', a, ", ", b,", ", c)

    print("\n------------------ Connection established, die rolling begins ------------------\n")
    
    while True:
        data = connection.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("From Bob: " + str(data))
        
        print("Sending my pedersen commitment")
        a_com = compute_pedersen_commitment(g, h, r, m)
        connection.send(str(a_com).encode())

        bobs_bit = connection.recv(1024).decode()
        print('Recieved Bob\'s sampled bit: ' + bobs_bit)

        print("Sending message and random number to Bob...")
        connection.send((str(generate_dice_roll())+","+str(r)).encode())

        dice_roll = str(agree_on_roll(m, int(bobs_bit)))
        print("The aggreeded dice roll is: " + dice_roll)
        print("Bye")

    connection.close()  # close the connection