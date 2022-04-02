Most of the time it's frustating that we need to download a Kernel source from [Samsung OSRC](https://opensource.samsung.com), and if we have a server that we build the Kernel on, we need to upload it into that server first. What a time-wasting, right?

Well, this script solves it! With this script, you can download the source directly from your Terminal! No need to download-reupload anymore. Just run, choose the source, and download 😎

> **Thanks to @fourkbomb and @Linux4 for code references!**

# Usage

First, we need to install Python 3 in order to run the script:

```bash
$ sudo apt install python3 -y
```

Then, clone and run it:

```bash
$ git clone https://github.com/hendramanudinata03/osrc_download.git
Cloning into 'osrc_download'...
...
$ cd osrc_download/
$ python osrc_download.py
```

It will ask you to choose device model and the specific source you want to download. soon after that, the download will start. Enjoy some snacks or a coffee, because it will take some time.

# Credits

[@fourkbomb](https://github.com/fourkbomb) and [@Linux4](https://github.com/Linux4) for much code references. Really, thank you!
