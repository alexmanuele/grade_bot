from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time
import pprint
import json
import sys
import smtplib, ssl
import pickle
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def main():
    #Get username and password from Command line
    if len(sys.argv) != 4:
        sys.exit(1)
    uname = sys.argv[1]
    pw = sys.argv[2]
    email = sys.argv[3]

    with open("credentials", "rb") as pickled:
        creds = pickle.load(pickled)

    bot = creds['email']
    bot_pass = creds['pw']
    ########### XPaths #################
    #XPath for Web For Students portal
    web_for_students = "/html/body/div[4]/table[1]/tbody/tr[1]/td[2]/a"
    #xpath for student_records
    student_records = "/html/body/div[4]/table[1]/tbody/tr[3]/td[2]/a"
    #xpath for final grades portal
    final_grades = "/html/body/div[4]/table[1]/tbody/tr[2]/td[2]/a"
    #xpath to submit grades request
    grades_button = "/html/body/div[4]/form/input"
    #path for student information
    student_info = "/html/body/div[4]/table[1]/caption"
    #path to select all course courses titles
    course_titles = "//div[4]/table[2]/tbody/tr/td[6]"
    #Path to select all course grades
    course_grades = "//div[4]/table[2]/tbody/tr/td[7]"
    ####################################

    #get the current working directory for file handling
    os.getcwd()

    #configure webdriver using Chrome Headless and Selenium
    option = webdriver.ChromeOptions()
    #Comment out the below line if you want to watch the webdriver.
    option.add_argument("--headless")

    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=option)
    driver.get("https://dalonline.dal.ca") #navigate to page
    driver.implicitly_wait(10)

    #driver related vars
    username_form = driver.find_element_by_id("username")#input area
    password_form = driver.find_element_by_id("password")
    login_btn = driver.find_element_by_xpath("//*[@id='fm1']/section[3]/input[4]")
    wait = WebDriverWait(driver, 10)

    username_form.clear() #remove anything stored by cookies
    username_form.send_keys(uname) #type in the user name passed by command line
    password_form.clear()
    password_form.send_keys(pw)
    wait = WebDriverWait(driver, 50)
    login_btn.click()

    #Make the browser wait until the new page is loaded.
    try:
        wait.until(EC.title_is('Dalhousie Online: Main Menu'))
    except:
        print("Time out waiting for web for Students")
        driver.quit()
        sys.exit(1)


    ####### LOGGED IN #########
    web_btn = driver.find_element_by_xpath(web_for_students)
    web_btn.click()
    #wait for page to load
    try:
        wait.until(EC.title_is('Dalhousie Online: Web for Students: Main Menu'))
    except:
        driver.quit()
        sys.exit(1)

    student_btn = driver.find_element_by_xpath(student_records)
    student_btn.click()
    try:
        wait.until(EC.title_is('Dalhousie Online: Web for Students: Student Records Menu'))
    except:
        driver.quit()
        sys.exit(1)

    ###### STUDENT RECORDS PAGE
    grades_btn = driver.find_element_by_xpath(final_grades)
    grades_btn.click()
    try:
        wait.until(EC.title_is('Final Grades'))
    except:
        driver.quit()
        sys.exit(1)

    ##### FINAL GRADES PAGE #####
    submit_btn = driver.find_element_by_xpath(grades_button)
    submit_btn.click()
    try:
        wait.until(
            EC.text_to_be_present_in_element((By.XPATH, student_info), "Student Information")
        )
    except:
        print("Time out waiting for grades")
        driver.quit()
        sys.exit(1)

    ####FINAL GRADES DISPLAY #####
    try:
        courses = driver.find_elements_by_xpath(course_titles)
        grades = driver.find_elements_by_xpath(course_grades)
    except Exception as e:
        print(e)
        sys.exit(0)



    course_desc = [i.text for i in courses]
    final_marks = [i.text for i in grades]

    query_results = dict(zip(course_desc, final_marks))

    #write the results to a json file
    with open("courses.json", "r") as file:
        previously_stored = json.load(file)

    if previously_stored == query_results:
        #grades havent been updated
        #print("Grades have not changed since last check")
        sys.exit(0)

    with open("courses.json", 'w') as file:
        file.write("\n")
        json.dump(query_results, file)

    #Send an email with the grades
    port = 465
    context = ssl.create_default_context()
    message = pprint.pformat(query_results)
    print("message contents:\n" + message)
    print("pprint output:")
    pprint.pprint(query_results)
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(bot, bot_pass)
        msg = MIMEMultipart()
        msg['From']=bot
        msg['To']=email
        msg['Subject']="Final grades update"
        msg.attach(MIMEText(message, 'plain'))
        #server.sendmail(email, email, message)
        server.send_message(msg)
    print("Success")
    driver.quit()

if __name__ == "__main__":
    main()
