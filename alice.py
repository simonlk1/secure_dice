import socket
import ssl
from shared import G, H, HOST, MESSAGE_DELIMITER, PORT, Q, agree_on_roll, generate_commit, generate_dice_roll, verify_commit


def serve():
    host = HOST
    port = PORT

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.vertify_mode = ssl.CERT_REQUIRED

    context.load_cert_chain("alice.tls.cert.pem", "alice.tls.key.pem")
    context.load_verify_locations("bob.tls.cert.pem")

    server = socket.socket()
    server.bind((host, port))
    server.listen()

    tls = context.wrap_socket(server, server_side=True)

    print("Awaiting connection")

    connection, address = tls.accept()

    print("Connection from: " + str(address))

    connection.do_handshake()

    print("Rolling my dice and committing it")

    roll = generate_dice_roll()
    c, r = generate_commit(roll)

    print("My roll is", roll, "\nMy commitment is",
          c, "\nMy random random value r is", r)

    print("Sending my commitment")

    connection.send(str(c).encode())

    bobs_commitment = connection.recv(1024).decode()
    print("Recieved Bob\'s commitment of", bobs_commitment)

    commitmentMsg = str(roll) + MESSAGE_DELIMITER + str(r)
    print("Sending my message and random number to Bob")

    connection.send(commitmentMsg.encode())

    [bobs_roll, bobs_r] = connection.recv(
        1024).decode().split(MESSAGE_DELIMITER)

    print("Bob rolled", bobs_roll, "with random value r of", bobs_r)

    if verify_commit(Q, G, H, int(bobs_r), int(bobs_roll), int(bobs_commitment)):
        print("Bob's commitment seems valid")
        dice_roll = agree_on_roll(roll, int(bobs_roll))
        print("We have agreed on the dice roll", dice_roll)

    else:
        print("Bob's commitment seems invalid")


if __name__ == '__main__':
    serve()
