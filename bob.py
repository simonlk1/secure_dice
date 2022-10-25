import socket
import ssl
from shared import Q, G, H, HOST, MESSAGE_DELIMITER, PORT, agree_on_roll, generate_dice_roll, verify_commit


def connect():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.vertify_mode = ssl.CERT_REQUIRED

    context.load_cert_chain("bob.tls.cert.pem", "bob.tls.key.pem")
    context.load_verify_locations("alice.tls.cert.pem")

    client = socket.create_connection((HOST, PORT))
    tls = context.wrap_socket(client, server_hostname="alice")

    tls.do_handshake()

    print("Connected to Alice at address", HOST, "port", PORT)

    alices_commitment = tls.recv(1024).decode()

    print('Received Alice\'s commitment:', alices_commitment)

    print("Rolling my dice")
    roll = generate_dice_roll()

    print("I rolled", roll)

    tls.send(str(roll).encode())

    print("Waiting for Alice's roll and random number")

    [alice_roll, alice_r] = tls.recv(1024).decode().split(MESSAGE_DELIMITER)

    print("Alice rolled", alice_roll, "with random value r of", alice_r)

    if verify_commit(Q, G, H, int(alice_r), int(alice_roll), int(alices_commitment)):
        print("Alice's commitment seems valid")
        dice_roll = agree_on_roll(int(alice_roll), roll)
        print("We have agreed on the dice roll", dice_roll)

    else:
        print("Alice's commitment seems invalid")

    tls.close()


if __name__ == '__main__':
    connect()
