# Track Tours
Do you want to get updates about when your favorite artists are playing shows in your area? Say less! Track Tours got you covered. Track Tours is a basic web scrapper that periodically checks the tour pages of provided artists and sends you an email when it finds any show that will be in your prefered cities.


## Requirements
- [Python3](https://www.python.org/)
- An email account(preferably Gmail)
- App password. More about that here: https://support.google.com/accounts/answer/185833?hl=en


## Install Required Packages
- Open terminal and navigate to the `/src`  dir
- Run `pip3 install -r requirements.txt`


## Configuration
- In `main.py`, edit the `artists` dictionary with your prefered artists and their tour pages
- Edit `desired_locations` with your prefered cities.
- I automatically set the wait time to a week but you can change that by providing your desired time to the `WAIT_TIME` constant.  

## Start Script
- In a terminal window, navigate to the `/src` dir and run `python3 main.py`
- You will be prompted for your email and password(App password). The script should start successfully after you provided valid values for both fields.

# TODO
- Create an efficient machanism to prevent unnecessary emails.
- Make it more non-programmer user friendly?
- Make it more background-run friendly?