import rsa
import socket
import ssl
from shared import ALICE_PORT, G, G, H, HOST, PORT, agree_on_roll, generate_dice_roll

with open('alice.public.pem', mode='rb') as alicepublicfile:
    keydata = alicepublicfile.read()

alicepub = rsa.PublicKey.load_pkcs1(keydata)

with open('bob.private.pem', mode='rb') as bobprivatefile:
    keydata = bobprivatefile.read()

bobpriv = rsa.PrivateKey.load_pkcs1(keydata)

def connect():
    host = HOST
    port = PORT

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    client = socket.create_connection((host, port))
    tls = context.wrap_socket(client)

    serverCertificate = tls.getpeercert()
    print(f"Certificate obtained from the Alice? {serverCertificate != None}")

    hShake = tls.do_handshake()
    print(f"Handshake done: {hShake == None}")

    a, b, c = tls.cipher()
    print('TLS cipher: ', a, ", ", b,", ", c)

    print("\n------------------ Connection established, die rolling begins ------------------\n")

    message = "Hi Alice"
    tls.send(message.encode())
    
    alice_commitment = tls.recv(1024).decode()

    print('Received Alice\'s commitment: ' + alice_commitment)
    
    print("Sampling a random bit...")
    random_bit = generate_dice_roll()
    tls.send(str(random_bit).encode())

    print("Waiting for Alice's message and random number...")
    opening = tls.recv(1024).decode()
    print("Alice's numbers are: " + opening)
    
    alice_data = opening.split(",")
    alice_sampled_bit = int(alice_data[0])
    alice_chosen = int(alice_data[1])

    if alice_commitment == str((G**alice_sampled_bit) * (H**alice_chosen)):
        print("Alice's commitment: VALID")
        dice_roll = str(agree_on_roll(alice_sampled_bit, random_bit))
        print("The aggreeded dice roll is: " + dice_roll)
        print("Bye")

    else:
        print("Alice's commitment: INVALID")
        tls.close()

    
    tls.close()