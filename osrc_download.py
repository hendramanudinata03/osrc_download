#!/usr/bin/python3
#
# osrc_download - Download a Samsung OSRC source release from Terminal (CLI)
# Based on work by Simon Shields <simon@lineageos.org> and Tim Zimmermann <tim@linux4.de>
#
# Copyright 2022 Hendra Manudinata <saya@hendra-manudinata.my.id>
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
from urllib.parse import quote
from bs4 import BeautifulSoup
from tqdm import tqdm

baseURL = "https://opensource.samsung.com"
searchURL = f"{baseURL}/uploadSearch?searchValue="
modalURL = f"{baseURL}/downSrcMPop?uploadId="
downSrcURL = f"{baseURL}/downSrcCode"

# Initialize `requests` session
session = requests.Session()

# Search query
# Access search page, get available `uploadId`,
# and store it in a dictionary along with `downloadPurpose`
searchQuery = input("Enter the search query: ")
requestSearch = session.get(searchURL + quote(searchQuery))
parseSearchContent = BeautifulSoup(requestSearch.content, "html.parser")
searchTable = parseSearchContent.find_all("table", class_="tbl-downList")
rowSearchTable = searchTable[0].find_all("tr", class_="")

dataList = []
global index
for index, row in enumerate(rowSearchTable):
    dataSearchTable = row.find_all("td")

    sourceModel = dataSearchTable[1].text.strip()
    sourceVersion = dataSearchTable[2].text.strip()
    sourceUploadId = dataSearchTable[5].find("a")["href"].split("'")[1]

    print(f"[{index + 1}] Model: {sourceModel} | Version: {sourceVersion}")

    dataList.append({
        "uploadId": sourceUploadId,
        "downloadPurpose": "AOP"
    })

# Choose source
requestDataNum = int(input(f"Select firmware [1 - {index + 1}]: "))
if len(dataList) >= requestDataNum and requestDataNum >= 1:
    requestData = dataList[requestDataNum - 1]
else:
    print("Invalid choice!")
    exit(1)

# Get remaining variable from modal page:
# `attachIds`, `_csrf`, `token`
requestModal = session.get(modalURL + requestData["uploadId"])
parseModalRequest = BeautifulSoup(requestModal.content, "html.parser")

requestData["attachIds"] = parseModalRequest.find_all("input", type="checkbox")[1]["id"]
requestData["_csrf"] = parseModalRequest.find_all(attrs={"name": "_csrf"})[0]["value"]
requestData["token"] = parseModalRequest.find_all(id="token")[0]["value"].encode("utf-8")

# Download the source
requestHeader = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55",
}
requestDown = session.post(downSrcURL, data=requestData, headers=requestHeader, stream=True)
sourceFileName = requestDown.headers["Content-Disposition"].split("=")[1][1:].replace('"', "").replace(";", "") # TODO: Better way of file name retrievement
sourceSize = int(requestDown.headers["Content-Length"])

try:
    print(f"\nDownloading {sourceFileName} ({sourceVersion}), please do not terminate the script!")
    progressBar = tqdm(total=sourceSize, unit="B", unit_scale=True)
    with open(sourceFileName, "wb") as file:
        for chunk in requestDown.iter_content(chunk_size=1024 * 1024):
            file.write(chunk)
            progressBar.update(len(chunk))
    progressBar.close()
    print("Done!")
except KeyboardInterrupt:
    progressBar.close()
    os.remove(sourceFileName)
    print("Interrupted!")
    exit(130)
except:
    progressBar.close()
    os.remove(sourceFileName)
    print("Error!")
    exit(1)
