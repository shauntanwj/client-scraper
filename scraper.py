import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException

class Browser: 
    browser, service, action = None, None, None
    
    # Browser Class Constructor
    def __init__(self, driver:str):

        # Initialize a service with a driver
        self.service = Service(driver)

        # Initialize the Chrome Driver
        self.browser = webdriver.Chrome(service=self.service)

        # Initialize a ActionChains object used to hover around menus
        self.action = ActionChains(self.browser)
        
    # Function to open the web page via the URL 
    def open_page(self, url:str):
        self.browser.get(url)

    # Function to close the web page
    def close_browser(self):
        self.browser.close()

    # A function to add input into different element
    # by: The class type to locate the element for instance LINK_TEXT, CLASS, ID, etc.
    # value: The value of the class type used to find the element
    # text: The desired input
    def add_input(self, by:By, value: str, text: str):
        field = self.browser.find_element(by=by, value=value)
        field.send_keys(text)
        time.sleep(1)

    # A function to click any element or button that is interactable
    # by: The class type to locate the element for instance LINK_TEXT, CLASS, ID, etc.
    # value: The value of the class type used to find the element
    def click_button(self, by:By, value: str):
        button = self.browser.find_element(by=by, value=value)
        button.click()
        time.sleep(1)

    # A function to login to a particular web page 
    # This function is just an example of a web page that contain a ID input field, and Password input field that is required to login to an account
    # id: This argument is just an example of any ID input field
    # password: This argument is just an example of any password input field
    def login(self, id:str, password: str):
        self.add_input(by=By.NAME, value="userid", text=id)
        self.add_input(by=By.NAME, value="password", text=password)
        self.click_button(by=By.CLASS_NAME, value="inputbutton")

    # A function to hover to the "Client" menu then to the "Client List" submenu and lastly click on "By Assured"
    # return: None
    def go_to_client(self):
        
        # Get the  "Client" element menu
        client = self.browser.find_element(by=By.XPATH, value='/html/body/table[2]/tbody/tr/td[1]/ul/li[4]/a')

        # Get the "Client List" element in the submenu
        client_list = self.browser.find_element(by=By.XPATH, value='/html/body/table[2]/tbody/tr/td[1]/ul/li[4]/ul/li[1]/a')
        
        # Get the "By Assured" element in the submenu
        by_assured = self.browser.find_element(by=By.XPATH, value='/html/body/table[2]/tbody/tr/td[1]/ul/li[4]/ul/li[1]/ul/li[1]')
        time.sleep(2)

        # Hover to the "Client" menu then the "Client List" submenu and lastly click on the "By Assured" button
        self.action.move_to_element(client).move_to_element(client_list).click(by_assured).perform()
        time.sleep(2)
    
    # A function to iterate through each alphabet from A-Z in the web page
    # return: None
    def iterate_alphabets(self):
        alphabet_uniq_id = 0

        # Initial XPATH of the alphabet "A"
        xpath = "/html/body/table[4]/tbody/tr/td/font/a[1]"

        # Loop through each alphabet from A-Z
        while alphabet_uniq_id < 26: 
            alphabet_uniq_id += 1
            self.click_button(by=By.XPATH, value=xpath)

            # Get the character of the alphabet
            chr_of_alphabet = chr(alphabet_uniq_id+64)

            # Calculate the number of rows in the table
            num_of_rows = self.calculate_rows()
            print("Current Iteration " + str(alphabet_uniq_id))
            print("Total Number of Clients starting with alphabet " + chr_of_alphabet + " is " + str(num_of_rows-1))
            
            # If there exist at least 1 client, name starting with the Alphabet
            # Then go through every single client and obtain the information of each client
            if num_of_rows > 1: 
                self.iterate_each_client_information(num_of_rows)

            has_next = True

            # Click on the "Next" button as long as it is interactable to go to the next page 
            while has_next: 
                try: 
                    self.click_button(by=By.LINK_TEXT, value="Next")
                    print("Click Next Button")

                    num_of_rows = self.calculate_rows()

                    if num_of_rows > 1: 
                        self.iterate_each_client_information(num_of_rows)
                    time.sleep(1)
                except NoSuchElementException: 
                    has_next = False
                    print("No Next Button")

            # Get the next XPATH   
            xpath = "/html/body/table[4]/tbody/tr/td/font/a[" + str(alphabet_uniq_id) + "]"
            time.sleep(1)

    # A function to calculate the rows of a table in the web page
    # return: the number of rows in the table
    def calculate_rows(self):
        num_of_rows = len(self.browser.find_elements(by=By.XPATH,value="/html/body/table[7]/tbody/tr"))
        return num_of_rows

    # A function to go through the information of every client
    # rows: total number of rows in the table shown on the web page
    # return: None
    def iterate_each_client_information(self, rows: int):
        for i in range(1, rows):
            client_uniq_id = str(i+1)
            name_with_title, name, residence_no, business_tel_no, mobile_tel_no = self.name_and_contact_number(client_uniq_id)
            email, correspondence_addr, residential_addr, business_addr = self.address(client_uniq_id)
            print("\nName with Title: " + name_with_title + "\nName: " + name + " \nResidence No: " + residence_no + " \n Business Tel No: " + business_tel_no + "\nMobile No: " + mobile_tel_no)
            print("Email: " + email + " \nCorrespondence Addr: " + correspondence_addr + " \n Residential Addr: " + residential_addr + "\nBusiness Addr: " + business_addr)
            self.write_to_file([i, name_with_title, name, residence_no, business_tel_no, mobile_tel_no, email, correspondence_addr, residential_addr, business_addr])
            time.sleep(1)

    # A function to obtain the name and the contact number of the client    
    # client_uniq_id: A unique ID to represent each client
    # return: The name with title, name, residence number, business telephone number and mobile telephone number   
    def name_and_contact_number(self, client_uniq_id: str):
      
        # The name shown on the table with title before clicking to the "Click Here" button
        name_xpath = "/html/body/table[7]/tbody/tr[" + client_uniq_id +  "]/td[1]/font/a[1]"
        name_with_title = self.browser.find_element(by=By.XPATH, value=name_xpath).text

        # The XPATH to check whether the "Click Here" button in the contact number column exist or not
        check_xpath = "/html/body/table[7]/tbody/tr[" + client_uniq_id +  "]/td[2]/font"

        # Check if there's a "Click Here" button for Contact Number
        # If the Contact Number column has a "-" text means there's no "Click Here" button 
        if self.browser.find_element(by=By.XPATH, value=check_xpath).text == "-": 
            name, residence_no, business_tel_no, mobile_tel_no = "-", "-", "-", "-"

            return name_with_title, name, residence_no, business_tel_no, mobile_tel_no

        # The XPATH for the "Click Here" button in the contact number column
        xpath = "/html/body/table[7]/tbody/tr[" + client_uniq_id +  "]/td[2]/font/a"
        
        # This Try and Except is used to ensure that after clicking the "Click Here" button, 
        # there exist a record of the contact number of the client or else handle the NoSuchElementException
        try: 
            self.click_button(by=By.XPATH, value=xpath)
            name = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[2]/font").text
            residence_no = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[4]/font").text
            business_tel_no = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[5]/font").text
            mobile_tel_no = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[6]/font").text
            
        except NoSuchElementException: 
            # If it shows "No Record Found", which will then throw a NoSuchElemenet Exception
            name, residence_no, business_tel_no, mobile_tel_no = "-", "-", "-", "-"
        finally: 
            time.sleep(1)
            self.browser.back()
            return name_with_title, name, residence_no, business_tel_no, mobile_tel_no
        
    # A function to obtain the address of the client  
    # client_uniq_id: A unique ID to represent each client
    # return: The email address, correspondence address, residential address and business address of the client
    def address(self, client_uniq_id: str):
        
        # The XPATH to check whether the "Click Here" button in the address column exist or not
        check_xpath = "/html/body/table[7]/tbody/tr[" + client_uniq_id +  "]/td[3]/font"

        # Check if there's a "Click Here" button for Contact Number
        # If the Address column has a "-" text means there's no "Click Here" button 
        if self.browser.find_element(by=By.XPATH, value=check_xpath).text == "-": 
            email, correspondence_addr, residential_addr, business_addr = "-", "-", "-", "-"
            return email, correspondence_addr, residential_addr, business_addr
        
        # The XPATH for the "Click Here" button in the address column
        xpath = "/html/body/table[7]/tbody/tr[" + client_uniq_id +  "]/td[3]/font/a"

        # This Try and Except is used to ensure that after clicking the "Click Here" button, 
        # there exist a record of the contact number of the client or else handle the NoSuchElementException
        try: 
            # If there's record found after clicking the Contact Number "Click Here" button
            self.click_button(by=By.XPATH, value=xpath)
            email = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[4]/font").text
            correspondence_addr = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[5]/font").text.replace("\n", " ")
            residential_addr = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[6]/font").text.replace("\n", " ")
            business_addr = self.browser.find_element(by=By.XPATH, value="/html/body/table[4]/tbody/tr[2]/td[7]/font").text.replace("\n", " ")
      
        except NoSuchElementException: 
            # If it shows "No Record Found", which will then throw a NoSuchElemenet Exception
            email, correspondence_addr, residential_addr, business_addr = "-", "-", "-", "-"
            
        finally:  
            # Scrape the address put inside a csv file
            time.sleep(1)
            self.browser.back()

            return email, correspondence_addr, residential_addr, business_addr
    
    # A function to write a row of data into a CSV file
    # row: An array of data
    # return: None
    def write_to_file(self, rows): 

        # Name of csv file 
        filename = "clients_information.csv"
            
        # Writing to csv file 
        with open(filename, 'a') as csvfile: 
            # Creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # Writing the data rows 
            csvwriter.writerow(rows)

            # Close the file
            csvfile.close()

        time.sleep(0.5)

    # Function for testing
    def find_element(self, by:By, value: str):
        xpath = "/html/body/table[4]/tbody/tr/td/font/a[1]"
        self.click_button(by=By.XPATH, value=xpath)
        try: 
            self.click_button(by=By.XPATH, value="/html/body/table[7]/tbody/tr[22]/td[3]/font/a")
        except NoSuchElementException: 
            print("Cannot Find Element")

if __name__ == '__main__':

    id="3038217"
    # id = "1002556"
    pw="4567Shaun"

    fields = ["No", "Name with Title", "Name", "Residence No", "Business Tel No", "Mobile Tel No", "Email", "Correspondence Addr", "Residential Addr", "Business Addr"]
    filename = "clients_information.csv"

    # Create the CSV file with the header/fields 
    with open(filename, 'a') as csvfile: 
        # Creating a csv writer object 
        csvwriter = csv.writer(csvfile) 
            
        # Writing the fields 
        csvwriter.writerow(fields) 

    browser = Browser("/Users/shauntan/Desktop/Python Project/client-scraper/chromedriver")
    browser.open_page("https://pruway.prudential.com.my/")
    
    time.sleep(3)

    browser.login(id=id, password=pw)
    time.sleep(2)

    browser.click_button(by=By.XPATH, value="/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/a")
    time.sleep(3)
    
    browser.go_to_client()

    time.sleep(2)

    browser.iterate_alphabets()
    time.sleep(10)

    browser.close_browser()



# Aplhabet T has multiple Next 
# Alphabet L has one Next
# Alphabet X has no records
