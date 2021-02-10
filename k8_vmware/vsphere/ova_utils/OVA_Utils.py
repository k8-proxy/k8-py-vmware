class OVA_Utils:

    def _headers_to_dict(self, response):
        result = {}
        if hasattr(response, 'getheaders'):
            for n, v in response.getheaders():
                result[n.lower()] = v.strip()
        else:
            for line in response.info().headers:
                if line.find(':') != -1:
                    n, v = line.split(': ', 1)
                    result[n.lower()] = v.strip()
        return result

    def get_ovffilename_from_path(self, tarfile, path):
        list = []
        file_names = tarfile.getnames()
        for name in file_names:
            if name == path:
                list.append(name)
        if list:
            return list[0]
        else:
            return None

    def get_ovafilename_from_pattern(self, tarfile):
        list = []
        file_names = tarfile.getnames()
        for f in file_names:
            if f.endswith(".ovf"):
                list.append(f)
        if list:
            return list[0]
        else:
            return None

