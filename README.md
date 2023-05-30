**Installation playwright**
How to install and use pytest-playwright for ubuntu

1. Use the following command to install pip for Python 3:
* 1.1 `sudo apt install python3-pip`
* 1.2 `pip3 —version`

2. Use the following command to install pytest for Python 3:
* `2.1 pip install pytest`

3. Use the following command to install pytest-playwright:
* 3.1  `pip install pytest-playwright`

4 Use the following command to install specific playwrught browser(chromium, firefox, webkit):
* 4.1 `playwright install`


5. Use the following command to install HTML reporter for pytest
* 5.1 `pip install pytest-html-reporter`

6. Use the following command to install multithread lib for pytest
* 6.1 `pip install pytest-xdist`

7. Use the local variable of ".env"
* 7.1 `pip install python-dotenv`



**Playwright CLI commands**

1. Start all tests by default params
* 1.1 `python3 -m pytest -s -v`

2. Start specific test (browser headless)
* 2.1 `python3 -m pytest -s -v test_some.py`

3. Start specific test by default browser (chromium)
* 3.1 `python3 -m pytest -s -v test_some.py --headed`

4. Start specific test by default browser (chromium) whit report after executing
* 4.1 `python3 -m pytest -s -v test_some.py --headed —html-report=./report.html`

5. Start specific test by default browser (chromium) whit report and multithread (3 core) executing
* 5.1 `python3 -m pytest -s -v test_some.py --headed —html-report=./report.html -n 3`

6. Start playwright codegen 
* `playwright codegen --viewport-size=1200,1200`, `playwright open google.com`

**Start playwright browser and create it instance**

exmaple how wee can use "headed mode" for chromium browser 

    from playwright.sync_api import Playwright, sync_playwright, expect
    def video_report(playwright: Playwright) -> None:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1600, 'height': 1024},
            record_video_dir="../Report/videos",
            record_video_size={"width": 800, "height": 600}
        )
        page = context.new_page()

* in first line we create function that takes playwright instance, which imported fom lib and it (func) return a void (None)
* further we declare var, whiсh assign instance of playwright chromium browser context with screensize, 
movie record folder, and movie size as arguments
* at last, we declare var which assign control playwright browser by incognito mode   

**Start browser whit userdata (profiles)** 

By default, playwright use - chromium browser by incognito mode, and we can't to save our *user data* for this behavior.   
We should to use ready user profile, that let us to call, playwright browser by user safety profile. 
I have created my default profile for fifrefox - browser and I get path for my FF user-data local storage use in FF command
>`about:profiles`

example how we can use FF profile  

    user_data_path = '/home/aser/.mozilla/firefox/n7rznrec.default-release'
    context = playwright.firefox.launch_persistent_context(user_data_dir=user_data_path ,headless=False, slow_mo=400)
    page = context.new_page()

* in this code we have declared path to local FF profile
* create instance browser context with user data and passing arguments to it
* create instance page browser whit user data (not incognito or robot-controlled)

This code, let us, to store user data, such: password for web app, session, cookie, localstorage JSON user-data 
If we used this way, we can reduce testlifetime, because it not necessary to spent time at sign up for every testrun.