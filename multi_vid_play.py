#! /opt/homebrew/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
options.add_argument('--disable-infobars')
options.add_argument("--start-maximized")
options.add_argument("--disable-notifications")

# Set up the browser driver
driver = webdriver.Chrome(options=options)

# Navigate to the Facebook login page
driver.get("https://www.facebook.com/login")
# Find the username and password fields and enter your login credentials

username_field = driver.find_element(by=By.ID, value="email")
password_field = driver.find_element(by=By.ID, value="pass")
username_field.send_keys("01327064885")
password_field.send_keys("@siamvai")
password_field.send_keys(Keys.RETURN)



# list of video URLs
urls = ['https://www.facebook.com/g4ming.otg/videos/810480416608880/',
        'https://www.facebook.com/g4ming.otg/videos/194144333447720/',
        'https://www.facebook.com/g4ming.otg/videos/257420673412631/']

# list to store the duration of each video
video_durations = []

#play and mute
def playNmute():
    # locate the div element
    div_element = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, '//*[@class="x1ey2m1c x9f619 xds687c x10l6tqk x17qophe x13vifvy x1ypdohk"]')))

    # perform the click using ActionChains
    ActionChains(driver).move_to_element(div_element).click().perform()

    # Locate mute dev element
    div_element_mute = WebDriverWait(driver, 300).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Mute']")))
    time.sleep(1)
    # Perform click on mute button
    ActionChains(driver).move_to_element(div_element_mute).click().perform()

def playedSofar():
    duration_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x14ctfv') and contains(@class, 'x1rg5ohu') and contains(@class, 'x1pg5gke') and contains(@class, 'xss6m8b') and contains(@class, 'x7h9g57') and contains(@class, 'x1t4t16n') and contains(@class, 'x8j4wrb') and contains(@class, 'x9hgts1') and contains(@class, 'x2b8uid') and contains(@class, 'x27saw0') and contains(@class, 'x3ajldb')]")))
    duration_list = duration_element.text.split("/")
    hours, minutes, seconds = map(int, duration_list[0].strip().split(':')) if len(duration_list[0].split(':')) == 3 else (0, ) + tuple(map(int, duration_list[0].strip().split(':')))
    duration_played = hours * 3600 + minutes * 60 + seconds
    print(duration_played)

# open each URL in a new tab and get the video duration
for url in urls:
    driver.execute_script("window.open('" + url + "', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    playNmute()
    # get the duration of the video
    duration_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'x14ctfv') and contains(@class, 'x1rg5ohu') and contains(@class, 'x1pg5gke') and contains(@class, 'xss6m8b') and contains(@class, 'x7h9g57') and contains(@class, 'x1t4t16n') and contains(@class, 'x8j4wrb') and contains(@class, 'x9hgts1') and contains(@class, 'x2b8uid') and contains(@class, 'x27saw0') and contains(@class, 'x3ajldb')]")))
    duration_list = duration_element.text.split("/")
    print(duration_list)

    hours, minutes, seconds = map(int, duration_list[1].strip().split(':')) if len(duration_list[1].split(':')) == 3 else (0, ) + tuple(map(int, duration_list[1].strip().split(':')))
    duration_seconds = hours * 3600 + minutes * 60 + seconds
   
    video_durations.append(duration_seconds)
    #driver.close()
    driver.switch_to.window(driver.window_handles[0])

driver.close()    
# list of video durations in seconds
#durations = video_durations
durations = [25, 50, 30]
print(durations)
time.sleep(5)
# switch to the last opened tab (the one with the longest video)
#driver.switch_to.window(driver.window_handles[-1])

# get the duration of the last video
#last_duration = durations[-1]
#print(last_duration)
# list to keep track of the remaining time for each video
remaining_times = [duration for duration in durations]

# play all videos
while True:
    # switch to the tab with the shortest remaining time
    shortest_idx = remaining_times.index(min(remaining_times))
    driver.switch_to.window(driver.window_handles[shortest_idx])
    playedSofar() 
    # wait for 1 second
    time.sleep(1)
    
    # update the remaining time for the current video
    remaining_times[shortest_idx] -= 1
    
    # check if the current video has ended
    if remaining_times[shortest_idx] == 0:
        # restart the current video
        driver.refresh()
        playNmute()        
        # update the remaining time for the current video
        remaining_times[shortest_idx] = durations[shortest_idx]
        
        # switch to the next tab
        next_idx = (shortest_idx + 1) % len(remaining_times)
        driver.switch_to.window(driver.window_handles[next_idx])


