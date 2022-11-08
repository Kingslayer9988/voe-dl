import os
import sys
import re
import requests
import json
import wget
from bs4 import BeautifulSoup

os.chdir(os.path.dirname(os.path.abspath(__file__))) #change directory to the exact path the script is located in

def download(URL):
    URL = str(URL)
    html_page = requests.get(URL)
    soup = BeautifulSoup(html_page.content, 'html.parser')

    name_find = soup.find("h1",class_="mt-1")  #parsing h1 tag for name of the mp4 file
    name = name_find.text
    name = name.replace(" ","")

    sources_find = soup.find_all(string = re.compile("const sources")) #searching for the script tag containing the link to the mp4
    sources_find = str(sources_find)
    slice_start = sources_find.index("const sources") 
    source = sources_find[slice_start:] #cutting everything before 'const sources' in the script tag
    slice_end = source.index(";")
    source = source[:slice_end] #cutting everything after ';' in the remaining String to make it ready for the JSON parser

    source = source.replace("const sources = ","")    #
    source = source.replace("\'","\"")                #Making the JSON valid
    source = source.replace("\\n","")                 #
    source = source.replace("\\","")                  #

    strToReplace = ","
    replacementStr = ""
    source = replacementStr.join(source.rsplit(strToReplace, 1)) #complicated but needed replacement of the last comma in the source String to make it JSON valid

    source_json = json.loads(source) #parsing the JSON 
    link = source_json["mp4"] #extracting the link to the mp4 file
    print(name)
    wget.download(link, out=f"output/{name}.mp4") #downloading the file
    print("\n")

if __name__ == "__main__":
    URL = sys.argv[1]
    download(URL)