#!/usr/bin/env python3
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

file = open("input.txt", "r")
polyglots = file.readlines()
file.close()

outputFile = open("output.txt", "w")

driver = webdriver.Safari()
driver.get('https://alf.nu/alert1')

inputField = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "inp")))
outputField = driver.find_elements_by_tag_name("label")[1]

scoreKeeper = {}

challengeList = driver.find_elements_by_tag_name("li")
challengeListLen = len(challengeList)
challengeIndex = 0
while challengeIndex < challengeListLen:
    outputFile.write('\nChallenge ' + challengeList[challengeIndex].text + '\n')
    print(challengeList[challengeIndex].text)

    for polyglot in polyglots:
        polyglot = polyglot.strip('\n')
        if polyglot not in scoreKeeper.keys():
            scoreKeeper[polyglot] = 0

        inputField = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "inp")))
        inputField.clear()
        inputField.send_keys(polyglot)

        time.sleep(0.3)
        outputField = driver.find_elements_by_tag_name("label")[1]
        if 'Win!' in outputField.text:
            outputFile.write("SUCCESS : " + polyglot + '\n')
            scoreKeeper[polyglot] += 1
        else:
            outputFile.write("FAILED : " + polyglot + '\n')

    challengeIndex += 1
    challengeList = driver.find_elements_by_tag_name("li")
    challengeListLen = len(challengeList)
    if challengeIndex < challengeListLen:
        challengeList[challengeIndex].click()

outputFile.write("\n------------------RESULTS------------------\n")
scoreKeeper = dict(sorted(scoreKeeper.items(), key=lambda item: item[1], reverse=True))
for polyglot, score in scoreKeeper.items():
    outputFile.write(polyglot + '    ' + str(score) + '\n')

print("Done")
outputFile.close()
driver.close()
