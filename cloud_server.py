import random

        #Machine Virtuel
class VirtualMachine:
    def __init__(self, vm_id, ram, cpu, storage_capacity):
        self.vm_id = vm_id
        self.ram = ram
        self.cpu = cpu
        self.storage_capacity = storage_capacity  # Capacité totale de stockage
        self.used_storage = 0  # Stockage utilisé
        self.files = {}  # Dictionnaire pour stocker les fichiers : {clé: contenu}

    def store_file(self, file_key, file_content):
        """Ajoute un fichier si l'espace le permet."""
        file_size = len(file_content)
        if self.used_storage + file_size > self.storage_capacity:
            return False, "Not enough storage space in VM."
        self.files[file_key] = file_content
        self.used_storage += file_size
        return True, "File stored successfully."

    def get_file(self, file_key):
        """Récupère un fichier par sa clé."""
        if file_key in self.files:
            return True, self.files[file_key]
        return False, "File not found."

    def delete_file(self, file_key):
        """Supprime un fichier."""
        if file_key in self.files:
            file_size = len(self.files[file_key])
            del self.files[file_key]
            self.used_storage -= file_size
            return True, "File deleted successfully."
        return False, "File not found."

    def list_files(self):
        """Liste tous les fichiers stockés."""
        return [{"key": key, "size": len(content)} for key, content in self.files.items()]

            #Hote
class Host:
    def __init__(self, host_id, os, arch, ram_capacity, vm_list):
        self.host_id = host_id
        self.os = os
        self.arch = arch
        self.ram_capacity = ram_capacity
        self.vm_list = vm_list  # Liste des VMs attachées à cet hôte

    def list_all_files(self):
        #Liste les fichiers sur toutes les VMs de cet hôte.
        all_files = []
        for vm in self.vm_list:
            all_files.extend(vm.list_files())
        return all_files

            #Datacenter
class Datacenter:
    def __init__(self, datacenter_id, host_list):
        self.datacenter_id = datacenter_id
        self.host_list = host_list  # Liste des hôtes dans ce datacenter

    def allocate_file(self, file_key, file_content):
        """Alloue un fichier à une VM disponible."""
        for host in self.host_list:
            for vm in host.vm_list:
                success, message = vm.store_file(file_key, file_content)
                if success:
                    return True, f"File stored in VM-{vm.vm_id} of Host-{host.host_id}."
        return False, "No available space in any VM."

    def list_all_files(self):
        """Liste tous les fichiers stockés dans le datacenter."""
        all_files = []
        for host in self.host_list:
            all_files.extend(host.list_all_files())
        return all_files

    def get_a_file(self, file_key):
        """Récupère le contenu d'un fichier dans toutes les VMs."""
        for host in self.host_list:
            for vm in host.vm_list:
                success, file_content = vm.get_file(file_key)
                if success:
                    return True, file_content
        return False, None  # Aucun fichier trouvé
    
    def delete_a_file(self, file_key):
        """supprimer un fichier."""
        for host in self.host_list:
            for vm in host.vm_list:
                success, message = vm.delete_file(file_key)
                if success:
                    return True, f"File deleted successfully."
        return False, "No surch file."

"""class Certificate:
    def __init__(self, certif1, certif2, certif3):
        self.machine_name=machine_name
        self.entreprise_name=entreprise_name
        self.serial_number=serial_number
        self.valide=valide
        self.domain=domain
        self.public_cypher_key=public_cypher_key

    def certificat_format(self, machine_name, entreprise_name, serial_number, valide, domain, public_cypher_key):
        certif=[machine_name, entreprise_name, serial_number, valide, domain, public_cypher_key]"""