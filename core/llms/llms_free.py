from selenium import webdriver
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import requests
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import getpass

URLS = {
  "pi": "https://pi.ai",
  "claude": "https://claude.ai",
  "GPT3": "https://chat.forefront.ai",
  "llama2":"https://labs.perplexity.ai/"
}

class llms_free:
  def __init__(self, model, profile_name):
    self.model = model
    options = webdriver.ChromeOptions()

    # Désactiver le message d'avertissement
    options.add_experimental_option("useAutomationExtension", False)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    # Options de navigation comme un utilisateur standard
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    # Récupérer le nom d'utilisateur
    username = getpass.getuser()

    if os.name == 'nt':
      profile_dir = rf'C:\Users\{username}\AppData\Local\Google\Chrome\User Data' 
    elif os.name == 'posix':
      profile_dir = rf'/home/t4u/.config/chromium/'
    else:
      profile_dir = rf'/Users/{username}/Library/Application Support/Google/Chrome'

    profile_path = os.path.join(profile_dir, profile_name)

    options.add_argument(f"user-data-dir={profile_path}")

    self.driver = webdriver.Chrome(options=options)
    print("Ouverture de Chromium...")
    #input()


  def open_chrome_profile(self, profile_name):
    print("Veuillez vous connecter aux different Provider puis appuyer sur Entrée.")
    input("Appuyez sur Entrée une fois que vous avez terminé...")
    print("Fermeture de Chromium...")
    # Fermer le navigateur
    self.driver.quit()

  def communicate_with_model(self,message):
    model = self.model
    if model=='pi':
      self.driver.get("https://pi.ai/talk")
      textarea_id="textarea"
      textarea = None

      try:
        # Attendre que le textarea soit présent dans le DOM
        textarea = WebDriverWait(self.driver, 480).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, textarea_id))
        )

        # Vérifier que le textarea est interactable
        WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, textarea_id))
        )

      except TimeoutException:

        # Le textarea n'est pas encore chargé, rafraichir la page
        self.driver.refresh()

        # Réessayer d'attendre le textarea
        textarea = WebDriverWait(self.driver, 480).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, textarea_id))
        )

        # Vérifier que le textarea est interactable
        WebDriverWait(self.driver, 1000).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, textarea_id))
        )

      if textarea is None:
        # Échec après 2 tentatives, lever une exception
        raise Exception(f"Failed to locate textarea {textarea_id}")

      else:
        # Faire défiler le textarea dans le viewport
        self.driver.execute_script("arguments[0].scrollIntoView()", textarea)

        # Attendre un court instant
        time.sleep(1)

        # Envoyer le message dans le textarea
        textarea.send_keys(message)
        textarea.send_keys(Keys.RETURN)

        # Attendre que le textarea soit interactable à nouveau
        while not textarea.is_enabled():
          time.sleep(1000)

        # Attendre que la réponse de l'AI soit affichée
        ai_response = WebDriverWait(self.driver, 1000).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, ".space-y-4"))
        )

        # Récupérer le texte de la réponse de l'AI
        response_text = ai_response.text
        print(response_text)
        # Retourner la réponse de l'AI
        return response_text
    elif model=='claude':
      self.driver.get("https://claude.ai/chat/f0e3b880-054c-4c23-9816-0a4d2809436b")
      textarea_id=".ProseMirror"
      textarea = None

      try:
        # Attendre que le textarea soit présent dans le DOM
        textarea = WebDriverWait(self.driver, 480).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, textarea_id))
        )

        # Vérifier que le textarea est interactable
        WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, textarea_id))
        )

      except TimeoutException:

        # Le textarea n'est pas encore chargé, rafraichir la page
        self.driver.refresh()

        # Réessayer d'attendre le textarea
        textarea = WebDriverWait(self.driver, 480).until(
          EC.presence_of_element_located((By.CSS_SELECTOR, textarea_id))
        )

        # Vérifier que le textarea est interactable
        WebDriverWait(self.driver, 10).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, textarea_id))
        )

      if textarea is None:
        # Échec après 2 tentatives, lever une exception
        raise Exception(f"Failed to locate textarea {textarea_id}")

      else:
        # Faire défiler le textarea dans le viewport
        self.driver.execute_script("arguments[0].scrollIntoView()", textarea)

        # Attendre un court instant
        time.sleep(1)
        textarea.send_keys(message)
        textarea.send_keys(Keys.RETURN)
        send_button = WebDriverWait(self.driver, 1000).until(
          EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Send Message"]'))
        )

        # Check if the send button is interactable
        if send_button.is_enabled():
          # Launch a function if the send button is interactable
          elements = self.driver.find_elements(By.CSS_SELECTOR, ".kQXewE")
          last_element = elements[-1]
          text = last_element.text

          print(text)

        else:
          # Wait for the send button to become interactable
          WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[aria-label="Send Message"]')))
          # Launch a function after the send button becomes interactable
          elements = self.driver.find_elements(By.CSS_SELECTOR, ".kQXewE")
          last_element = elements[-1]
          text = last_element.text

          print(text)

        
  #_get host session cookies 
  def get_host_session_cookie(self):
    print("Open pi page")
    self.driver.get(URLS[self.model])
    input('Click enter when you finish')
    cookies = self.driver.get_cookies()
    for cookie in cookies:
      if cookie['name'] == '__Host-session':
        host_cookie = cookie
        break

    cookie_dict = {
      'name': host_cookie['name'],
      'value': host_cookie['value'],
      'domain':host_cookie['domain'],
    }
  
    cookie_json = json.dumps([cookie_dict])
  
    with open('host_cookie.json', 'w') as f:
      f.write(cookie_json)
    self.driver.quit()
    #return cookie_json


  def retrieve_host_session_cookie(self):
    with open('host_cookie.json', 'r') as f:
      cookie = json.load(f)
      cookie = cookie[0]
    self.driver.get(URLS[self.model])
    #wait page load totally before add cookies 
    time.sleep(9)
    cookie_str = f"{cookie['name']}={cookie['value']}; domain={cookie['domain']}; path=/"
    js = f"document.cookie = '{cookie_str}';"
    # Execute JavaScript to set cookie
    self.driver.execute_script(js)
    input('Click enter when you finish') 
    return self.driver

#claude
#test = llms_free('pi', 'Default')
#test.communicate_with_model('Bonjour comment allez vous ?')

class Model:
    def __init__(self, model_name, master_prompt, api_key):
        self.model_name = model_name
        self.master_prompt = master_prompt
        self.api_key = api_key

    def generate_text(self, prompt):
        if self.api_key:
            communicator = llms_free(self.model_name, self.profile_name)
        else:
            communicator = llms_free(self.model_name, self.profile_name)

        response = communicator.communicate_with_model(prompt)

        if self.api_key:
            return response
        else:
            print("It's free! 😂")