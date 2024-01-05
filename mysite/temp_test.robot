*** Settings ***
Library     SeleniumLibrary

*** Test Cases ***
Open Google.com
    [Documentation]    Open Google homepage in Chrome browser
    Open Browser    https://google.com    chrome
    Maximize Browser Window
