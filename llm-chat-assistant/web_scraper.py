#------------------------------------------------------------------------------------------------
# This script scrapes the FAQs from the Budget Direct website and saves the data to a CSV file.
# The script uses Selenium to automate the web scraping process and BeautifulSoup to parse the HTML.
# The script first extracts the URLs of all FAQ categories from the main FAQ page.
# It then loops through each category, extracts the questions and answers, and stores the data in a DataFrame.
# Finally, the data is saved to a CSV file.
# The script is designed to run in headless mode to avoid opening a browser window.
# The script is also configured to run in a containerized environment.
# The script requires the ChromeDriver executable to be installed on the system.
# The ChromeDriver executable can be downloaded from https://sites.google.com/a/chromium.org/chromedriver/downloads.
# The path to the ChromeDriver executable should be specified in the script.
#------------------------------------------------------------------------------------------------
# Author: Behzad Asadi
# Date: March 2025
#------------------------------------------------------------------------------------------------
#%% Importing libraraies

import time
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

#%% Configure Chrome options

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--no-sandbox")  # Required for running in containers
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
chrome_options.add_argument("--window-size=1920,1080")  # Set window size

# Specify the path to ChromeDriver
chrome_service = Service("/usr/local/bin/chromedriver")

# Initialize the WebDriver
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

# URL of the main FAQ page
base_url = "https://www.budgetdirect.com.au"
main_url = f"{base_url}/car-insurance/car-insurance-faqs.html"

# Open the main FAQ page
driver.get(main_url)
time.sleep(5)  # Wait for the page to load

# Parse the page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")

# Find all category links
category_links = soup.find_all(name="a", class_="column__link", href=True)
categories = [
    {"name": link.text.strip(), "url": base_url + link["href"]}
    for link in category_links if "car-insurance-faqs" in link["href"]
]


# Initialize a DataFrame to store the results
faq_data = []

# Loop through each category and scrape FAQs
for category in categories:
    if category["name"] != '':
        print(f"Scraping category: {category['name']}")
        driver.get(category["url"])
        time.sleep(random.uniform(3, 6))  # Random delay to avoid being blocked

        # Parse the category page
        category_soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Find all FAQ containers
        faq_containers = category_soup.find_all(name="div", class_="faq-container__content")

        for container in faq_containers:
            # Extract the question
            question_div = container.find('div', class_='faq-container__question')
            if question_div:
                question = question_div.find('h3').get_text(strip=True)
            else:
                question = 'No question found'

            # Extract the answer paragraphs
            # Extract the answer div
            answer_div = container.find('div', class_='faq-container__answer')

            answer_parts = []

            if answer_div:
                # Use .stripped_strings to extract all text content from the answer div
                answer_parts = list(answer_div.stripped_strings)
                answer = ' '.join(answer_parts)
            else:
                answer = 'No answer found'
            
            faq_data.append({'question': question, 'answer': answer})
        
# Convert the data to a pandas DataFrame
faq_df = pd.DataFrame(faq_data)

# Save the data to a CSV file
faq_df.to_csv("faqs.csv", index=False)

# Close the WebDriver
driver.quit()

print("Scraping completed. Data saved to 'faqs.csv'.")
# %%
