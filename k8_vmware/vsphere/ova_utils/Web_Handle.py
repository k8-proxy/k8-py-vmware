from six.moves.urllib.request import Request, urlopen

from k8_vmware.vsphere.ova_utils.OVA_Utils import OVA_Utils
class Web_Handle(object):
    def __init__(self, url):
        self.url = url
        self.helper=OVA_Utils()

        r = urlopen(url)
        if r.code != 200:
            raise FileNotFoundError(url)

        self.headers = self.helper._headers_to_dict(response=r)
        if 'accept-ranges' not in self.headers:
            raise Exception("Site does not accept ranges")
        self.st_size = int(self.headers['content-length'])
        self.offset = 0

    def tell(self):
        return self.offset

    def seek(self, offset, whence=0):
        if whence == 0:
            self.offset = offset
        elif whence == 1:
            self.offset += offset
        elif whence == 2:
            self.offset = self.st_size - offset
        return self.offset

    def seekable(self):
        return True

    def read(self, amount):
        start = self.offset
        end = self.offset + amount - 1
        req = Request(self.url,
                      headers={'Range': 'bytes=%d-%d' % (start, end)})
        r = urlopen(req)
        self.offset += amount
        result = r.read(amount)
        r.close()
        return result

    # A slightly more accurate percentage
    def progress(self):
        return int(100.0 * self.offset / self.st_size)