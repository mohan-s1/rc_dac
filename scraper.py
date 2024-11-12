#/* --------------------------------------------------------------------------------
#   UVA Research Computing
#   University of Virginia
#   Matthew Galitz, Mohan Shankar
#
#   This file scrapes UVA websites for information about faculty
#-------------------------------------------------------------------------------- */
import requests
from bs4 import BeautifulSoup
import pandas as pd
#-------------------------------------------------------------------------------- */
# FUNCTION DEFINITIONS

def get_page_title(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the <h1> tag with the specific class and id
        page_title = soup.find('h1', class_='page_title', id='page_title')
        
        # Extract and return the text if the tag is found
        if page_title:
            return page_title.get_text(strip=True)
        else:
            print("The page title element was not found.")
            return None
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None
    
def get_emails(url):
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Use a set to ensure unique emails
        emails = {a['href'].replace('mailto:', '') for a in soup.find_all('a', class_='people_meta_detail_info_link') if a['href'].startswith('mailto:')}
        
        # Check if any emails were found and print an appropriate message
        if emails:
            print("Emails found:")
            for email in emails:
                print(email)
        else:
            print("No emails found.")
            emails.add(url) # append url to email set if no email is found
        
        return list(emails)  # Convert the set back to a list if needed
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return url
    
#-------------------------------------------------------------------------------- */
# SCRAPE ENGINEERING FACULTY
eng_url_list = [] # list to house all engineering faculty url

for i in range(3): # set max range to 35 since there are
    url = f'https://engineering.virginia.edu/faculty?page={str(i)}'
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all 'a' tags with the class 'contact_block_name_link'
        links = [a['href'] for a in soup.find_all('a', class_='contact_block_name_link') if 'href' in a.attrs]
        
        # Print the extracted URLs
        for link in links:
            print(link)
            eng_url_list.append(link)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

base_engineering_url = "https://engineering.virginia.edu/"

eng_faculty_names = []

eng_faculty_emails = []

for i, link in enumerate(eng_url_list):
    url = base_engineering_url+link
    name = get_page_title(url)
    emails = get_emails(url)
    
    if name:
        eng_faculty_names.append(name)
    
    for email in emails:
        eng_faculty_emails.append(email)

eng_data = {'Faculty Name': eng_faculty_names, 
        'Faculty Email': eng_faculty_emails, 
        'Engineering Page': eng_url_list}

eng_df = pd.DataFrame(eng_data)

print(eng_df)
#-------------------------------------------------------------------------------- */
# MED SCHOOL DEPARTMENTS
# General pattern of https://med.virginia.edu/dept/faculty/

# Neuroscience does https://med.virginia.edu/neuroscience/faculty/primary-faculty/ distinguishing primary and joint faculty. 
# Pharmacology has a similar trend https://med.virginia.edu/pharm/primary-faculty/ but they also have https://med.virginia.edu/pharm/postdocs/ 
# Public Health Sciences has https://med.virginia.edu/phs/office-of-the-chair/
# Lastly, Microbiology, Immunology, and Cancer Biology has Primary Faculty and Research Faculty
# https://med.virginia.edu/mic/faculty/primary-faculty/ and https://med.virginia.edu/mic/faculty/research-faculty/


med_dept_list = ["bmg", "physiology-biophysics", "cell-biology", "genome-sciences"]