import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import cv2


# Initialize the WebDriver
def start_game():
    # Set up Chrome WebDriver
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=r'C:\Path\to\chromedriver',
                              options=options)  # Set the correct path to chromedriver
    driver.get("https://elgoog.im/t-rex/")  # Open the Dino game URL

    # Wait for the game to load (waiting for canvas element to be visible)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))

    # Start the game by simulating the space key to start the dino
    body = driver.find_element("tag name", "body")
    body.send_keys(Keys.SPACE)

    return driver


# Detect obstacles and jump
def detect_and_jump():
    # Capture the screen where the game is running
    screen = np.array(ImageGrab.grab())

    # Convert the screen to grayscale for simpler processing
    gray_screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    # You can define a threshold based on the pixels of the game area where the obstacles are
    # For simplicity, we assume that obstacles are darker objects on a light background
    obstacle_pixels = np.sum(gray_screen < 150)  # Check for dark pixels

    # If enough dark pixels are detected, assume there is an obstacle and jump
    if obstacle_pixels > 1000:  # Adjust this threshold depending on your screen and obstacle detection area
        pyautogui.press('space')  # Jump


# Main game loop
def run_game():
    driver = start_game()

    try:
        while True:
            detect_and_jump()  # Detect obstacles and jump if needed
            time.sleep(0.1)  # Small delay to mimic human reaction time
    except KeyboardInterrupt:
        print("Game over!")
        driver.quit()


if __name__ == "__main__":
    run_game()