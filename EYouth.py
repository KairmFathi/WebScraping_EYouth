#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# !pip install python-dotenv --quiet
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import load_dotenv
import pandas as pd
import time
import os
import sys

# Load environment variables from the .env file
load_dotenv()

# Access the env_file data
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Initializing and configuring a data frame to save the result
result_df = pd.DataFrame(columns=["No.", "Video title", "Video link"])
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns

# Setup the hidden browser option
hide_browser = Options()
hide_browser.add_argument('--headless=new')
hide_browser.add_argument('--mute-audio')

# Initiate the browser object and load the URL
browser= Chrome(options= hide_browser)
browser.get('https://dfpp.eyouthlearning.com/')

# Login step
Login_btn= browser.find_element(By.XPATH, "//div/a [@class= 'btn-primary rounded-2xl font-medium px-4 py-2 w-fit h-fit' ]")
Login_btn.click()
data_fld= browser.find_element(By.XPATH, "//div/input [@class = 'w-full' ]")
data_fld.send_keys(email, Keys.TAB, password, Keys.ENTER)  

# navigating to course page
time.sleep(5)
course_fld= browser.find_elements(By.XPATH, "//li [@class = 'w-full list-none' ]")[4]
course_fld.click()

# Define a list of all videos' titles
time.sleep(5)
title_list = [ x.text for x in (browser.find_elements(By.XPATH, "//div/ul/li \
                                                      [contains (@class,'CourseVideoLessons_lessonItem__LsrrA CourseVideoLessons_activeLesson__RNi+O') \
                                                      or contains (@class, 'CourseVideoLessons_lessonItem__LsrrA')]"))]

# Initialize "next video" object 
next_video = browser.find_element(By.XPATH, "//button[@class='py-2 px-1 bg-[#FFFFFF] absolute top-[50%] translate-y-[-50%] end-0  ']")

# Navigate through the other videos and load each video details to the Result_df
serial = 0
counter = 1
while counter <= len(title_list):
  time.sleep(2)
  vid_link= (browser.find_element(By.XPATH, "//div/div/iframe")).get_attribute('src')
  vid_name = title_list[serial]
  result_df.loc[len(result_df)] = [serial, vid_name, vid_link]
  next_video.click()
  serial+=1
  counter+=1

# Displaying result data frame 
# print(result_df.to_string(index=False))
result_df.sample(5)

# Saving the results as an excel sheet on the desktop and, if not permitted, will be at the same location of the notebook
file_name = " EYouth freelancing course"  + ".xlsx"
result_df.to_excel(file_name, index=False)

print ("\n Process completed, data and videos scapped successfully")
    
browser.close()


# In[80]:


result_df.tail(5)

