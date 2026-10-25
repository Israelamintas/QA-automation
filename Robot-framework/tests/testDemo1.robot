*** Settings ***
Documentation    To validate the login form
Library  SeleniumLibrary
#Resource

*** Test Cases ***
Validate UnSuccesful login
    Open Mortgage Login Page
#    Fill the login form
#   wait until it cheks and display error message
#  verify the error message is correct

*** Keywords ***
Open Mortgage Login Page
    Create WebDriver  Edge
    Go To  https://rahulshettyacademy.com/loginpagePractise/
