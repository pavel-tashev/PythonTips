On a recent project I ran into an issue with Python, Selenium and Webdriver. I wanted to achieve a very simple task, to open a link in a new tab and to close it after that.

I tried to find a proper solution on the Internet but it turned out that depending on the Webdrive, the version of Python and Selenium, this simple task can face different issues.

This is why I want to share with you a solution I developed and which worked for me.

Here is what I use:
* Python 3.6.x
* Selenium 3.141.x
* Webdriver = Chrome

Tasks:
“Open a URL with Chrome (let’s call with **A**), and right after that open a second URL (let’s call it **B**) in a new tab, close the tab with URL **B** and go back the first tab with URL **A**.”

Solution:
* First import this:
```
from selenium import webdriver
```
* And here is the code:
```
# Define the URL's we will open and a few other variables 
main_url = 'https://www.linkedin.com' # URL A
tab_url = 'https://www.google.com' # URL B
chromedriver = 'DESCTINATION_TO_YOUR_CHROME_DRIVER'

# Open main window with URL A
broswer= webdriver.Chrome(chromedriver)
broswer.get(main_url)
print("Current Page Title is : %s" %broswer.title)

# Open a new window
broswer.execute_script("window.open('');")

# Switch to the new window and open URL B
broswer.switch_to.window(broswer.window_handles[1])
broswer.get(tab_url)
# …Do something here
print("Current Page Title is : %s" %broswer.title)

# Close the tab with URL B
broswer.close()

# Switch back to the first tab with URL A
broswer.switch_to.window(broswer.window_handles[0])
print("Current Page Title is : %s" %broswer.title)
```

I hope that helps!
