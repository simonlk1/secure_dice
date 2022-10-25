import socket
import ssl
from shared import Q, G, H, HOST, MESSAGE_DELIMITER, PORT, agree_on_roll, generate_commit, generate_dice_roll, verify_commit


def connect():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.vertify_mode = ssl.CERT_REQUIRED

    context.load_cert_chain("bob.tls.cert.pem", "bob.tls.key.pem")
    context.load_verify_locations("alice.tls.cert.pem")

    client = socket.create_connection((HOST, PORT))
    tls = context.wrap_socket(client, server_hostname="alice")

    tls.do_handshake()
    connection = tls

    print("Connected to Alice at address", HOST, "port", PORT)

    alices_commitment = connection.recv(1024).decode()

    print('Received Alice\'s commitment:', alices_commitment)

    print("Rolling my dice and committing it")
    roll = generate_dice_roll()
    c, r = generate_commit(roll)

    print("My roll is", roll, "\nMy commitment is",
          c, "\nMy random random value r is", r)

    print("Sending my commitment")

    connection.send(str(c).encode())

    [alices_roll, alices_r] = connection.recv(
        1024).decode().split(MESSAGE_DELIMITER)

    print("Alice rolled", alices_roll, "with random value r of", alices_r)

    commitmentMsg = str(roll) + MESSAGE_DELIMITER + str(r)
    print("Sending my message and random number to Alice")

    connection.send(commitmentMsg.encode())

    if verify_commit(Q, G, H, int(alices_r), int(alices_roll), int(alices_commitment)):
        print("Alice's commitment seems valid")
        dice_roll = agree_on_roll(int(alices_roll), roll)
        print("We have agreed on the dice roll", dice_roll)

    else:
        print("Alice's commitment seems invalid")

    tls.close()


if __name__ == '__main__':
    connect()
