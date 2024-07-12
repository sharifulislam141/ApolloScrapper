from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time, random, csv

username = 'tusar77@albayouk.com.sa'
password = 'jhfdkjsafsafA1'

driver = webdriver.Chrome()

driver.get('https://app.apollo.io/#/login')
time.sleep(20)

userElement = driver.find_element(By.CSS_SELECTOR, 'input[name="email"]').send_keys(username)
passElement = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]').send_keys(password)
time.sleep(random.randint(2, 3))
login_Button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
time.sleep(5)
driver.get('https://app.apollo.io/#/people?finderViewId=6674b20eecfedd00018453a1&contactEmailStatusV2[]=verified&page=1&organizationNumEmployeesRanges[]=1%2C10&personTitles[]=ceo&personLocations[]=United%20States&organizationIndustryTagIds[]=5567cd4773696439dd350000')
time.sleep(5)

def next_page():
    button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="right-arrow"]')
    actions = ActionChains(driver)
    actions.move_to_element(button).perform()
    button.click()
    time.sleep(5)

def scroll_feed_until_end():
    feed_div = driver.find_element(By.CSS_SELECTOR, 'div.zp_DUflC')
    last_height = driver.execute_script("return arguments[0].scrollHeight", feed_div)
    while True:
        driver.execute_script("arguments[0].scrollTo(0, arguments[0].scrollHeight);", feed_div)
        time.sleep(3)
        new_height = driver.execute_script("return arguments[0].scrollHeight", feed_div)
        if new_height == last_height:
            break
        last_height = new_height

def save_to_csv(data):
    keys = data[0].keys()
    with open('output.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

data = []

try:
    while True:
        scroll_feed_until_end()
        main_content = driver.find_element(By.CSS_SELECTOR, 'div.zp_DUflC')
        tbodys = main_content.find_elements(By.CSS_SELECTOR, 'tbody.zp_RFed0')

        for tbody in tbodys:
            try:
                name = tbody.find_element(By.CSS_SELECTOR, 'div.zp_xVJ20 a').text
            except:
                name = "N/A"
            
            try:
                links = tbody.find_elements(By.CSS_SELECTOR, 'a.zp-link.zp_OotKe')
                person_Linkedin = links[0].get_attribute('href')
                person_Twitter = links[1].get_attribute('href')
                company_Website = links[2].get_attribute('href')
                company_Linkedin = links[3].get_attribute('href')
            except:
                person_Linkedin = person_Twitter = company_Website = company_Linkedin = "N/A"
            
            try:
                company = tbody.find_element(By.CSS_SELECTOR, 'a.zp_WM8e5.zp_kTaD7').text
            except:
                company = "N/A"
            
            try:
                basicinfo = tbody.find_elements(By.CSS_SELECTOR, 'span.zp_Y6y8d')
                title = basicinfo[0].text
                contact_location = basicinfo[1].text
                employes = basicinfo[2].text
            except:
                title = contact_location = employes = "N/A"
            
            try:
                parent_div = tbody.find_element(By.CSS_SELECTOR, '.zp_paOF8')
                spans = parent_div.find_elements(By.CSS_SELECTOR, 'span.zp_PHqgZ.zp_TNdhR')
                text_list = [span.text.strip() for span in spans]
                industries = ', '.join(text_list)
            except:
                industries = "N/A"

            try:
                parent_div2 = tbody.find_element(By.CSS_SELECTOR, '.zp_HlgrG.zp_y8Gpn.zp_uuO3B')
                spans2 = parent_div2.find_elements(By.CSS_SELECTOR, 'span.zp_yc3J_.zp_FY2eJ')
                text_list2 = [span.text.strip() for span in spans2]
                keywords = ', '.join(text_list2)
            except:
                keywords = "N/A"
            
            data.append({
                'Name': name,
                'Person Linkedin': person_Linkedin,
                'Person Twitter': person_Twitter,
                'Company Website': company_Website,
                'Company Linkedin': company_Linkedin,
                'Company': company,
                'Title': title,
                'Contact Location': contact_location,
                'Employees': employes,
                'Industries': industries,
                'Keywords': keywords
            })

        next_page()

except KeyboardInterrupt:
    print("Process interrupted by user. Saving data...")
    save_to_csv(data)
    driver.quit()
except Exception as e:
    print(f"An error occurred: {e}")
    save_to_csv(data)
    driver.quit()
finally:
    save_to_csv(data)
    driver.quit()
