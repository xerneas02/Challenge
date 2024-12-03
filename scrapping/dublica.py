import os
import hashlib

def hash_file(filepath):
    """
    Calcule le hachage MD5 d'un fichier pour identifier les doublons.
    :param filepath: Chemin du fichier à hacher.
    :return: Hachage MD5 du fichier.
    """
    hasher = hashlib.md5()
    try:
        with open(filepath, 'rb') as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"Erreur lors du hachage du fichier {filepath}: {e}")
        return None

def clean_directory(directory):
    """
    Supprime les fichiers en double dans un dossier donné.
    :param directory: Chemin du dossier à nettoyer.
    """
    if not os.path.exists(directory):
        print(f"Le dossier {directory} n'existe pas.")
        return

    seen_hashes = {}
    duplicates = []

    # Parcourir tous les fichiers du dossier
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_hash = hash_file(filepath)
            if file_hash:
                if file_hash in seen_hashes:
                    duplicates.append(filepath)
                else:
                    seen_hashes[file_hash] = filepath

    # Supprimer les fichiers en double
    for duplicate in duplicates:
        try:
            os.remove(duplicate)
            print(f"Fichier dupliqué supprimé : {duplicate}")
        except Exception as e:
            print(f"Erreur lors de la suppression de {duplicate}: {e}")

    print(f"Nettoyage terminé. {len(duplicates)} fichiers en double supprimés.")

# Exemple d'utilisation
output_dir = "oyster"  # Remplacez par le chemin de votre dossier
clean_directory(output_dir)
