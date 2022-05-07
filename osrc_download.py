#!/usr/bin/env python3
#
# osrc_download - Download a Samsung OSRC source release from Terminal
# Based on work by Simon Shields <simon@lineageos.org> and Tim Zimmermann <tim@linux4.de>
#
# Copyright 2022 Hendra Manudinata <hendra@manudinata.me>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

baseURL = "https://opensource.samsung.com"
searchURL = "https://opensource.samsung.com/uploadSearch?searchValue=%s"
modalURL = "https://opensource.samsung.com/downSrcMPop?uploadId=%s"
downSrcURL = "https://opensource.samsung.com/downSrcCode"

searchQuery = input("Enter the search query: ")

session = requests.Session()

requestSearch = session.get(searchURL % quote(searchQuery))
parseSearchContent = BeautifulSoup(requestSearch.content, "lxml")

searchTable = parseSearchContent.find_all("table", class_="tbl-downList")
rowSearchTable = searchTable[0].find_all("tr", class_="")

dataIndex = 1
dataList = {}

for row in rowSearchTable:
    dataSearchTable = row.find_all("td")

    sourceModel = dataSearchTable[1].text.strip()
    sourceBaseband = dataSearchTable[2].text.strip()
    sourceUploadId = dataSearchTable[5].find("a")["href"].split("'")[1]

    print("[%d] Model: %s | Baseband Version: %s" % (dataIndex, sourceModel, sourceBaseband))

    dataList[dataIndex] = {
        "uploadId": sourceUploadId
    }

    dataIndex += 1

# Correct the index
dataIndex -= 1

dataChoiceNum = int(input("Select firmware [1 - %d]: " % dataIndex))

try:
    dataChoice = dataList[dataChoiceNum]
except KeyError:
    print("Invalid choice!")
    exit(1)

requestModal = session.get(modalURL % dataChoice["uploadId"])
parseModalRequest = BeautifulSoup(requestModal.content, "lxml")

dataChoice["attachIds"] = parseModalRequest.find_all("input", type="checkbox")[1]["id"]
dataChoice["_csrf"] = parseModalRequest.find_all(attrs={"name": "_csrf"})[0]["value"]
dataChoice["token"] = quote(parseModalRequest.find_all(id="token")[0]["value"].encode("utf-8"))

dataParams = "_csrf=" + dataChoice["_csrf"] + "&uploadId=" + dataChoice["uploadId"] + "&attachIds=" + dataChoice["attachIds"] + "&downloadPurpose=AOP&token=" + dataChoice["token"]
dataInBytes = [ord(s) for s in dataParams]

dataHeaders = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Content-Length": "" + str(len(dataInBytes)),
    "Origin": baseURL,
    "Referer": searchURL % quote(searchQuery),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55",
}

requestDown = session.post(downSrcURL, data=dataParams, headers=dataHeaders, stream=True)

sourceFileName = requestDown.headers["Content-Disposition"].split("=")[1][1:].replace('"', "").replace(";", "")
splittedFileName = sourceFileName.split("_")

print("")
print("Model: " + splittedFileName[0])
print("Region: " + splittedFileName[1])
print("Android version: " + splittedFileName[2])
print("File name: " + sourceFileName)
print("")

try:
    print("Downloading, please do not terminate the script!")
    with open(sourceFileName, "wb") as file:
        for chunk in requestDown.iter_content(chunk_size=512 * 1024):
            file.write(chunk)
    print("Done!")
except KeyboardInterrupt:
    os.remove(sourceFileName)
    print("Interrupted!")
    exit(130)
except:
    print("Error!")
    exit(1)
