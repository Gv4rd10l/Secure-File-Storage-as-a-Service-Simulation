from concurrent import futures
import grpc
import cloud_service_pb2
import cloud_service_pb2_grpc
from cloud_server import Datacenter, VirtualMachine, Host
import socket
import pickle
import os
import threading
from crypto_test import Cryptographie
#from code_base import CodeBase

class CloudServiceServicer(cloud_service_pb2_grpc.CloudServiceServicer):
    def InteractiveSession(self, request_iterator, context):
        """Session interactive entre le client et le serveur."""
        print("Starting interactive session with the client...")

        # Configuration du datacenter pour l'interaction
        vm1 = VirtualMachine(vm_id=1, ram=16, cpu=4, storage_capacity=1000)
        vm2 = VirtualMachine(vm_id=2, ram=32, cpu=8, storage_capacity=4000)
        vm3 = VirtualMachine(vm_id=1, ram=32, cpu=8, storage_capacity=3000)
        vm4 = VirtualMachine(vm_id=2, ram=64, cpu=16, storage_capacity=6000)
        vm5 = VirtualMachine(vm_id=3, ram=16, cpu=4, storage_capacity=2000)
        vm6 = VirtualMachine(vm_id=4, ram=16, cpu=4, storage_capacity=1000)
        
        host1 = Host(host_id=1, os="Windows 10", arch="x32", ram_capacity=2048, vm_list=[vm2, vm6])
        host2 = Host(host_id=2, os="Windows_server_2012", arch="x86", ram_capacity=7048, vm_list=[vm4])
        host3 = Host(host_id=3, os="Debian_11", arch="x86", ram_capacity=1024, vm_list=[vm3])
        host4 = Host(host_id=4, os="Ubuntu_server", arch="x86", ram_capacity=2048, vm_list=[vm1, vm5])

        datacenter = Datacenter(datacenter_id=1, host_list=[host1, host2, host3, host4])
        #datacenter2 = Datacenter(datacenter_id=2, host_list=[host2, host4])

        yield cloud_service_pb2.ServerOutput(
            output="\n--- Cloud Operations ---\n[1] Store a file\n[2] List all files\n[3] Get a file content\n[4] Delete a file\n[5] Exit\nEnter your choice: "
        )

        for command in request_iterator:
            user_input = command.input.strip()
            if user_input == "1":
                yield cloud_service_pb2.ServerOutput(output="Enter file name: ")
                file_name = next(request_iterator).input.strip()
                yield cloud_service_pb2.ServerOutput(output="Enter file content: ")
                file_content = next(request_iterator).input.strip()
                success, message = datacenter.allocate_file(file_name, file_content)
                yield cloud_service_pb2.ServerOutput(output=message)
            elif user_input == "2":
                files = datacenter.list_all_files()
                if files:
                    file_list = "\n".join([f"{file['key']} ({file['size']} bytes)" for file in files])
                else:
                    file_list = "No files available."
                yield cloud_service_pb2.ServerOutput(output=f"Files in the cloud:\n{file_list}")
            elif user_input == "3":
                yield cloud_service_pb2.ServerOutput(output="Enter file name: ")
                file_name = next(request_iterator).input.strip()
                success, content = datacenter.get_a_file(file_name)
                if success:
                    yield cloud_service_pb2.ServerOutput(output=f"Content of {file_name}: {content}")
                else:
                    yield cloud_service_pb2.ServerOutput(output="File not found.")
            elif user_input == "4":
                yield cloud_service_pb2.ServerOutput(output="Enter file name: ")
                file_name = next(request_iterator).input.strip()
                success, message = datacenter.delete_a_file(file_name)
                yield cloud_service_pb2.ServerOutput(output=message)
            elif user_input == "5":
                yield cloud_service_pb2.ServerOutput(output="Session terminated.")
                break
            else:
                yield cloud_service_pb2.ServerOutput(
                    output=" .Invalid choice. Try again.\n--- Cloud Operations ---\n[1] Store a file\n[2] List all files\n[3] Get a file content\n[4] Delete a file\n[5] Exit\nEnter your choice: "
                )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=8))
    cloud_service_pb2_grpc.add_CloudServiceServicer_to_server(CloudServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051.")
    server.wait_for_termination()

def certif_auth_service(func1, func2):

    print("           ___________________________________________________________________________________________________________________________")
    print("           ___________________________________________________________________________________________________________________________")
    print("           |----------         -------------        --------------------                                                 -------------")
    print("           |                   |   ---------        --------   ---------                                                 |  ----------")
    print("           |  |-------         |  |                        |   |                                                         |  |         ")
    print("           |  |                |  |                        |   |                  ----                 ----              |  |         ")
    print("           |  --------         |  ---------|               |   |                  |  |                 |  |              |  ---------|")
    print("           |  --------         |--------|  |               |   |                 |    |               |    |             |--------|  |")
    print("           |  |                         |  |               |   |                |______|             |______|                     |  |")
    print("           |  |                ----------  |               |   |               |        |           |        |           ---------   |")
    print("           |  |                ------------|               |   |              |          |         |          |          ------------|")
    print("           ___________________________________________________________________________________________________________________________")
    print("           ___________________________________________________________________________________________________________________________")


    certif = {"machine_name":"machine_cloud_pepe", "entreprise_name":"pepe_cloud", "serial_number":"89045GFQLK341", "valide":"31/12/25", "domain":"pepecloud.com", "public_cypher_key":"567hbbgghhjjhu4567899VBNjjuhbfbhfj"}
    certif1 = {"machine_name":"machine_cliente_neymar", "entreprise_name":"neymar_client", "serial_number":"6954GHS43", "valide":"31/12/25", "domain":"pepecloud.com", "public_cypher_key":"njecinfhffefefolz123Thhv"}
    certif2 = {"machine_name":"machine_cliente_gvardiol", "entreprise_name":"gvardiol_client", "serial_number":"8563GJG90", "valide":"09/01/25", "domain":"pepecloud.com", "public_cypher_key":"jeukshtrfrk5674fdhn90klz"}
    certif3 = {"machine_name":"machine_cliente_rodry", "entreprise_name":"rodry_client", "serial_number":"9853IKG65", "valide":"12/02/25", "domain":"pepecloud.com", "public_cypher_key":"lshgvfbnat4560lfnjgf342s"}
    liste_certif_client = [certif1, certif2, certif3]
    
    def debut(liste_certif_client, certif):

        def handle_client(conn, addr):
            """Fonction pour gérer chaque client dans un thread séparé."""
            print(f"Connexion établie avec {addr}")

            try:
                public_key_recv = conn.recv(8192)

                pem_public_key_client = pickle.loads(public_key_recv)
                print("-------------------------------------------------------------------------------------------------------------------------")
                print("clé publique reçu: ", pem_public_key_client)
                print("-------------------------------------------------------------------------------------------------------------------------")
                public_key_client_loaded = Cryptographie.load_public_key(pem_public_key_client)
                public_key_send = pickle.dumps(pem_public_key_cloud)
                conn.sendall(public_key_send)
                #print("clé publique 1ere transformation : ")
                
                #try:
                data_received = conn.recv(9096)
                if not data_received:
                    print("Aucune donnée reçue. Fermeture de la connexion.")
                    return
                certify = pickle.loads(data_received)
                #certify = decrypto(certif_decrypt, private_key_cloud_loaded)
                print(f"Certificat reçu de {addr} : {certify}")
                
                data_to_send = pickle.dumps(certif)
                conn.sendall(data_to_send)
                print("Certificat envoyé au client :", certif)

                if certify in liste_certif_client:
                    func1(conn, func2, public_key_client_loaded)
                else :
                    print("------------------------------------------------------------------------")
                    print("--------info : an untrust machine try to connect and got block !--------")
                    print("------------------------------------------------------------------------")
                    conn.sendall(pickle.dumps("Certificat invalide. Connexion refusée."))
                    pass

            except Exception as erreur:
                print("une erreur s'est produite: ", erreur)
            finally:
                conn.close()
                print(f"Connexion avec {addr} terminée.")

        def connexion():
            host = 'localhost'
            port = 5000

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                    server_socket.bind((host, port))
                    server_socket.listen(5)
                    print(f"Serveur en écoute sur {host}:{port}")

                    while True:
                        # Accepter une nouvelle connexion client
                        conn, addr = server_socket.accept()
                        # Démarrer un nouveau thread pour gérer ce client
                        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                        client_thread.start()

            except Exception as e:
                print(f"Erreur du serveur : {e}")
        connexion()

    debut(liste_certif_client, certif)

def Authentif_client(conn, serve, pub_key):
    User1={"username":"Neymar", "password":"BestPlayer"}
    User2={"username":"Gvardiol", "password":"BestDefence"}
    User3={"username":"Rodry", "password":"BestMiddle"}
    User_list=[User1, User2, User3]
    try:

        conn.sendall(pickle.dumps("Enter your username: "))
        username_unpickle = pickle.loads(conn.recv(1024)).strip()
        decrypted_message = decrypto(username_unpickle, private_key_cloud_loaded)
        username = decrypted_message
        
        conn.sendall(pickle.dumps("Enter your password: "))
        password_unpickle = pickle.loads(conn.recv(1024)).strip()
        decrypted_message = decrypto(password_unpickle, private_key_cloud_loaded)
        password = decrypted_message

        for user in User_list:
            if user["username"] == username and user["password"] == password:
                message_retour = "Authentication successful."
                encrypted_message = crypto(message_retour, pub_key)
                conn.sendall(pickle.dumps(encrypted_message))
                serve()
                return
        
        conn.sendall(pickle.dumps("Authentication failed."))
        return False

    except Exception as e:
        print(f"Erreur lors de l'authentification : {e}")
        conn.sendall(pickle.dumps("Authentication failed due to an error."))
        return False

def init_crypto():
    # Génération des clés
    private_key_cloud, public_key_cloud = Cryptographie.generate_keys()

    # Sérialisation pour simulation
    pem_public_key_cloud = Cryptographie.serialize_public_key(public_key_cloud)
    pem_private_key_cloud = Cryptographie.serialize_private_key(private_key_cloud)

    # Chargement des clés (simulation)
    public_key_cloud_loaded = Cryptographie.load_public_key(pem_public_key_cloud)
    private_key_cloud_loaded = Cryptographie.load_private_key(pem_private_key_cloud)

    return public_key_cloud_loaded, private_key_cloud_loaded, pem_public_key_cloud

def crypto(message1, cle_pub):

    # Chiffrement avec clé publique cliente
    encrypted_message = Cryptographie.encrypt_message(cle_pub, message1)
    return encrypted_message

def decrypto(message2, cle_priv):

    # Déchiffrement avec clé privée cloud
    try:
        decrypted_message = Cryptographie.decrypt_message(private_key_cloud_loaded, message2)
    except Exception as e:
        decrypted_message = "Erreur lors du déchiffrement :"
        print(decrypted_message, e)
    return decrypted_message

public_key_cloud_loaded, private_key_cloud_loaded, pem_public_key_cloud = init_crypto()

if __name__ == "__main__":
    certif_auth_service(Authentif_client, serve)