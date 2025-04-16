import grpc
import cloud_service_pb2
import cloud_service_pb2_grpc
import socket
import pickle
import os
from crypto_test import Cryptographie 
#from code_base import CodeBase

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cloud_service_pb2_grpc.CloudServiceStub(channel)

        def request_generator():
            while True:
                user_input = input()  # Prend une commande utilisateur
                yield cloud_service_pb2.ClientInput(input=user_input)
                if user_input.strip() == "5":
                    break

        # Établissement d'une session interactive
        print("Connected to the cloud. Starting interactive session...")
        response_iterator = stub.InteractiveSession(request_generator())

        for response in response_iterator:
            print(response.output, end="")  # Affiche les réponses du serveur

def secu(run, crypto, private_key, pem_public_key):

    neymar_certif_pepe={"machine_name":"machine_cliente_neymar", "entreprise_name":"neymar_client", "serial_number":"6954GHS43", "valide":"31/12/25", "domain":"pepecloud.com", "public_cypher_key":"njecinfhffefefolz123Thhv"}
    cloud_certif={"machine_name":"machine_cloud_pepe", "entreprise_name":"pepe_cloud", "serial_number":"89045GFQLK341", "valide":"31/12/25", "domain":"pepecloud.com", "public_cypher_key":"567hbbgghhjjhu4567899VBNjjuhbfbhfj"}

    def auth_user(client_socket, pub_key_cloud, private_key):
        #print(public_key_cloud_loaded)
        username_prompt = pickle.loads(client_socket.recv(1024))
        print(username_prompt, end="")
        username = input()
        encrypted_message = crypto(pub_key_cloud, username)
        client_socket.sendall(pickle.dumps(encrypted_message))

        password_prompt = pickle.loads(client_socket.recv(1024))
        print(password_prompt, end="")
        password = input()
        encrypted_message = crypto(pub_key_cloud, password)
        client_socket.sendall(pickle.dumps(encrypted_message))

        encrypted_auth_response = pickle.loads(client_socket.recv(1024))
        #print(encrypted_auth_response)
        decrypted_message = decrypto(encrypted_auth_response, private_key_client_loaded)
        auth_response = decrypted_message
        print(auth_response)
        if auth_response == "Authentication successful.":
            print("Démarrage de la session gRPC...")
            run()  # Lance la session gRPC
        else:
            print("Échec de l'authentification.")

        #run()

    def check_certif(neymar_certif, auth_user):

        host = 'localhost'
        port = 5000

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                client_socket.connect((host, port))
                print(f"Connecté à {host}:{port}")

                public_key_send = pickle.dumps(pem_public_key)
                client_socket.sendall(public_key_send)
                public_key_recv = client_socket.recv(8192)
                pem_public_key_cloud = pickle.loads(public_key_recv)
                print("-------------------------------------------------------------------------------------------------------------------------")
                print("clé publique du serveur cloud : ", pem_public_key_cloud)
                print("-------------------------------------------------------------------------------------------------------------------------")
                public_key_cloud_loaded = Cryptographie.load_public_key(pem_public_key_cloud)

                data_to_send = pickle.dumps(neymar_certif)
                client_socket.sendall(data_to_send)

                data_received = client_socket.recv(8192)
                certif = pickle.loads(data_received)

                print("-------------------------------------------------------------------------------------------------------------------------")
                print("Certificat reçu du serveur : ", certif)
                print("-------------------------------------------------------------------------------------------------------------------------")

                if certif==cloud_certif:
                    auth_user(client_socket, public_key_cloud_loaded, private_key)
                elif certif!=cloud_certif:
                    decid = input("we can't trust this cloud certification do you want to continuous and connect ?(y/n): ")
                        #decid=string(decid)
                    if decid=="y":
                        #print(public_key_cloud_loaded)
                        auth_user(client_socket, public_key_cloud_loaded, private_key)
                    elif decid=="n":
                        print("disconnecting...")
                    else :
                        print("------choice not availabe------")
                else :
                    print("----we can't get the cloud certificate----")

        except Exception as erreur:
            print("une erreur s'est produite: ", erreur)

    check_certif(neymar_certif_pepe, auth_user)

def init_crypto():
    # Génération des clés
    private_key_client, public_key_client = Cryptographie.generate_keys()

    # Sérialisation pour simulation
    pem_public_key_client = Cryptographie.serialize_public_key(public_key_client)
    pem_private_key_client = Cryptographie.serialize_private_key(private_key_client)

    # Chargement des clés (simulation)
    public_key_client_loaded = Cryptographie.load_public_key(pem_public_key_client)
    private_key_client_loaded = Cryptographie.load_private_key(pem_private_key_client)

    return public_key_client_loaded, private_key_client_loaded, pem_public_key_client

def crypto(cle_pub, message1):

    # Chiffrement avec clé publique cloud
    encrypted_message = Cryptographie.encrypt_message(cle_pub, message1)
    
    return encrypted_message

def decrypto(message2, cle_priv):

    # Déchiffrement avec clé privée cliente (clé correspondant à clé publique cliente)
    # Note : Ce déchiffrement est simulé. Vous devez chiffrer un autre message avec public_key_client.
    try:
        decrypted_message = Cryptographie.decrypt_message(private_key_client_loaded, message2)
    except Exception as e:
        decrypted_message = "Erreur lors du déchiffrement: "
        print(decrypted_message, e)

    return decrypted_message

public_key_client_loaded, private_key_client_loaded, pem_public_key_client = init_crypto()

if __name__ == "__main__":
    secu(run, crypto, private_key_client_loaded, pem_public_key_client)