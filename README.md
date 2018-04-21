# fuji
Creates a free trial account on [Fujitv.live](https://fujitv.live/) that lasts a day so I don't have to.

`short_alpha_words.txt` is an edited version of [dwyl/english-words/words_alpha](https://github.com/dwyl/english-words/blob/master/words_alpha.zip), only containing words under 10 characters long.

I'm not in any way affiliated with Fujitv.live.

```
usage: driver.py [-h] [--hidden] [-o] [-c CHROMEDRIVER_PATH]

Creates an account on Fujitv.live.

optional arguments:
  -h, --help            show this help message and exit
  --hidden              Hide the ChromeDriver.
  -o, --open-logon      Open the login page.
  -c CHROMEDRIVER_PATH, --chromedriver-path CHROMEDRIVER_PATH
                        Provides the location of ChromeDriver. Should probably
                        be the full path.
```

An example execution, that hides selenium and opens the login page after completion: 

`python3 driver.py --hidden -oc /usr/local/bin/chromedriver`

Output:

```
Registered Successfully.
UngyveLugVentersPelotaGogos518@mailinator.com
835WTdOkbGQL1cm5F
```


### Selenium Instructions

For Windows, download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads), and put the path on command line (escape backslashes):

`python3 driver.py --hidden -oc C:\\temp\\chromedriver.exe`

---

[Script for Linux](https://gist.github.com/ziadoz/3e8ab7e944d02fe872c3454d17af31a5)

ChromeDriver location should be `/usr/local/bin/chromedriver` if installed with that script, but may be `/usr/lib/chromium-browser/chromedriver` otherwise.

---

Mac with [brew](https://brew.sh/):

`sudo brew install chromedriver`

Located at `/usr/local/bin/chromedriver`
