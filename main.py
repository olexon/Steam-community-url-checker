################
### SETTINGS ###
################

api_key = "YOUR_API_KEY"    #you can get it at https://steamcommunity.com/dev/apikey by registering any domain
worksers = 5                                    #changes the amount of tasks perforemed at the same time (more = faster but can cause some issues)

###############################################
###         SOURCE CODE STARTS HERE         ###
### CHANGING ANYTHING CAN BREAK THE SCRIPT! ###
###############################################

import requests
import concurrent.futures
import sys

from datetime import datetime

available_urls = list()

def IsAvailable(apikey, url):
    if len(url) < 3 or len(url) > 32:
        return("Wrong URL length!")

    try:
        response = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={}&vanityurl={}".format(apikey, url)).json()

        data = response["response"]["success"]

        if data != 42:
            return(False)
        else:
            return(True)
    except Exception:
        return("There was an error while trying to get response from STEAM")

def Main(url):
    check_url = IsAvailable(api_key, url.strip())

    if check_url == True:
        print("ID Found ( {} )".format(url.strip()))
        available_urls.append("{} - Available".format(url.strip()))
    elif check_url == False:
        print("Unavailable ( {} )".format(url.strip()))
    elif isinstance(check_url, str):
        print(check_url)
        

if __name__ == "__main__":
    try:
        get_userdata = sys.argv[1]
    except IndexError:
        print("You didn't specify a file!")
        quit()

    specified_file = open(get_userdata, "r")
    urls = specified_file.readlines()
    specified_file.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=worksers) as executor:
        future = {executor.submit(Main, url): url for url in urls}

    time_now = datetime.now().strftime("%d-%m-%Y-%H%M%S")
    output = open("output-{}.txt".format(time_now), "w")

    for item in available_urls:
        formatted_output = "{}\n".format(item)
        output.write(formatted_output)

    print("\nOutput file has been created!")
    output.close()