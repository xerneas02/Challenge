import os
import time
import hashlib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Créer un dossier pour enregistrer les images
output_dir = "amanita"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Configurer Selenium avec Chrome
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Exécuter Chrome en mode sans interface graphique
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

nb_images = 0

def generate_filename(image_url):
    """Génère un nom de fichier valide à partir de l'URL."""
    hash_object = hashlib.md5(image_url.encode())  # Hacher l'URL pour générer un nom unique
    filename = f"{hash_object.hexdigest()}.jpg"
    return filename

def download_image(image_url, output_dir):
    """Télécharge et enregistre une image avec un nom de fichier valide."""
    try:
        import requests
        filename = generate_filename(image_url)
        output_path = os.path.join(output_dir, filename)
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Image téléchargée : {output_path}")
        else:
            print(f"Erreur de téléchargement : {image_url}, code {response.status_code}")
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image {image_url}: {e}")

def scrape_images(page_url, output_dir):
    """Scrape les images depuis une page avec Selenium."""
    global nb_images
    try:
        driver.get(page_url)
        time.sleep(5)  # Attendre que la page soit complètement chargée
        # Trouver toutes les balises d'image dans les balises <picture> ou <source>
        images = driver.find_elements(By.TAG_NAME, "source")
        for img in images:
            src = img.get_attribute("srcset")
            if src:
                image_url = src.split(",")[0].split(" ")[0]  # Obtenir l'URL principale
                download_image(image_url, output_dir)
                nb_images += 1
    except Exception as e:
        print(f"Erreur lors du scraping de {page_url}: {e}")

# URL de la page de départ
base_url = "https://www.istockphoto.com/fr/photos/amanita-mushroom?page="

# Scraper les 2 premières pages pour tester
for page in range(1, 101):  # Limiter à 2 pages pour test
    url = base_url + str(page)
    print(f"Scraping page {page}...")
    scrape_images(url, output_dir)
    if nb_images >= 7000:
        break

# Fermer le navigateur
driver.quit()

print("Scraping terminé.")
