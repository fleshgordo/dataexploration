import requests
from bs4 import BeautifulSoup
import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

# Selenium setup
options = Options()
#options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

policies = [
    "INVESTMENT", "TRADE", "FINANCE", "TAX", "ENTERPRISE", "ANTI_CORRUPTION",
    "EDUCATION", "EMPLOYMENT", "INNOVATION", "DIGITAL", "TRANSPORT", "ENERGY",
    "ENVIRONMENT", "AGRICULTURE", "TOURISM"
]

base_url = "https://westernbalkans-competitiveness.oecd.org/dimensions/"
urls = [f"{base_url}{policy}/" for policy in policies]

# Open CSV file for writing
with open('subdimension_text.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Dimension', 'Title', 'Subdimension', 'Subdimension Title', 'Dimension Text'])

    for index,url in enumerate(urls):
        # Load page with Selenium
        driver.get(url)
        
        # Wait until elements with data-state="closed" are present and click them
        time.sleep(5)

        selector = f"document.querySelectorAll('button[data-state=\"closed\"][id*=\"{policies[index]}\"]');"
        # Use JavaScript to select and click elements
        script = f'''
        let elements = {selector} 
        elements.forEach(element => element.click());
        '''
        print("-> opened all sub-menus via JS")
        driver.execute_script(script)

        # Give some time for dynamic content to load after clicking
        time.sleep(2)

        # Use BeautifulSoup to parse the page after clicking
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the main dimension policy text
        policy_dimension = soup.find('p', class_='font-bernini text-base font-normal md:text-lg whitespace-pre-wrap text-left').get_text()
        policy_title = soup.find('h1', class_='font-caecilia text-4xl font-normal leading-normal md:text-7xl whitespace-pre-wrap text-left').get_text()

        policy_text = "N/A"
        # Find the description text for policy
        policy_elem = soup.find('section', class_='content-wide').find("p")
        if (policy_elem):
            policy_text = policy_elem.get_text()

        print(f"writing policy: {policy_dimension} title: {policy_title}")
        writer.writerow([policy_dimension,policy_title,"","",policy_text])
        
        # Find and process Sub-Dimension sections
        target_paragraphs = soup.find_all('p', string=re.compile(r'Sub-Dimension \d+\.\d+'))

        # Find divs with data-state="open" and "radix" in the id
        # need them for the subdimension text
        divs = soup.find_all('div', {'data-state': 'open', 'id': lambda x: x and 'radix' in x})

        # for each subdivision ...
        for index,target_paragraph in enumerate(target_paragraphs):
            sub_dimension_text = target_paragraph.get_text()
            following_paragraph = target_paragraph.find_next('p')
            dimension_text = divs[index].find('p').get_text()
            following_text = following_paragraph.get_text() if following_paragraph else "N/A"
            print(f"writing policy: {policy_dimension} sub: {sub_dimension_text}")
            # Write sub-dimension details to CSV
            writer.writerow([policy_dimension,policy_title,sub_dimension_text, following_text, dimension_text])

driver.quit()
print("Data saved to subdimension_text.csv")