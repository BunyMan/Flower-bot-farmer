from urllib.request import urlopen


def interneton():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except:
        return False


print(interneton())
