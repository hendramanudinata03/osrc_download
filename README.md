<div align="center">
    <h1>osrc_download</h1>
</div>

Most of the time it's frustating that we need to download a releases from [Samsung OSRC](https://opensource.samsung.com), especially Kernel sources. And if we have a server that we build the source on, we need to upload it into there first. What a time-wasting, right?

Well, this script solves it! With this script, you can download the release directly from your Terminal! No need to download-reupload anymore. Just run, choose the release, and download 😎

# Installation

First, we need to install Python 3, PIP, and Git in order to run the script.

For example, for Debian-based Linux distribution:

```
# apt install python3 python3-pip git -y
```

Then, clone the repository:

```
$ git clone https://github.com/hendramanudinata03/osrc_download.git
Cloning into 'osrc_download'...
...
$ cd osrc_download/
```

Before running the script for the first time, please install required dependencies:

```
$ pip install -r requirements.txt
```

Now you can run the script:

```
$ python osrc_download.py
```

It will ask you to choose device model and the specific source you want to download. Soon after that, the download will start. Enjoy some snacks or a coffee, because it will take some time.

# Credits

[@fourkbomb](https://github.com/fourkbomb) for his [Gist](https://gist.github.com/fourkbomb/9f0aeadb5b300a4fdd23559c368d75dd) and [@Linux4](https://github.com/Linux4) for his [SamsungFirmwareBot component](https://github.com/Linux4/SamsungFirmwareBot/blob/master/src/main/java/de/linux4/samsungfwbot/SamsungKernelInfo.java). Really, thank you for the references!
