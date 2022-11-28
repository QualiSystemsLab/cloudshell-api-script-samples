from urllib.request import urlopen, Request, build_opener, HTTPHandler
import re
import ntpath

from multipart_formdata import MultiPartForm


class QualiApi(object):
    def __init__(self, host, username, password, domain="Global", port="9000"):
        self.host = host
        self.port = port

        self.opener = build_opener(HTTPHandler)

        login_url = 'http://{0}:{1}/API/Auth/Login'.format(host, port)
        data = 'username={0}&password={1}&domain={2}' \
            .format(username,
                    password.replace('+', '%2B').replace('/', '%2F').replace('=', '%3D'),
                    domain)
        request = Request(url=login_url, data=bytes(data))
        request.add_header('Content-Type', 'application/x-www-form-urlencoded')
        backup = request.get_method
        request.get_method = lambda: 'PUT'
        url = self.opener.open(request)
        self.token = url.read()
        self.token = re.sub(r'^"', '', self.token)
        self.token = re.sub(r'"$', '', self.token)
        request.get_method = backup

    def upload_test_to_shared(self, test_location, target_location):
        """
        :param test_location:
        :param target_location: folder hierarchy in shared folder. the path should be separated with /.
         if empty, test will be created in root shared folder.
        :type test_location: str
        :type target_location: str
        :return:
        """
        if target_location.startswith('Shared'):
            target_location = target_location.lstrip('Shared').lstrip('/')

        head, tail = ntpath.split(test_location)
        filename = tail or ntpath.basename(head)

        form = MultiPartForm()

        with open(test_location) as file_handle:
            form.add_file('test', filename, fileHandle=file_handle)

        body = str(form)
        url = 'http://{0}:{1}/API/Scheduling/Tests/Shared/{2}'.format(self.host, self.port, target_location)
        request = Request(url)
        request.add_header('Content-type', form.get_content_type())
        request.add_header('Content-length', str(len(body)))
        request.add_header('Authorization', 'Basic {}'.format(self.token))
        request.data = body

        try:
            response = self.opener.open(request)
            result = response.read()
        except Exception as e:
            print(str(e))
            raise e

        return result

    def delete_test_from_shared(self, test_location):
        url = 'http://{0}:{1}/API/Scheduling/Tests/Shared/{2}'.format(self.host, self.port, test_location)
        request = Request(url)
        request.get_method = lambda: 'DELETE'
        request.add_header('Authorization', 'Basic {}'.format(self.token))

        try:
            response = self.opener.open(request)
            result = response.read()
        except Exception as e:
            print(str(e))
            raise e

        return result

    """
    def delete_single_test_from_shared(test_location):
        api = QualiApi('localhost', '9000', 'admin', 'admin', 'Global')
        result = api.delete_test_from_shared(test_location)
        # verify response (result)
        print 'success'
    """

    def get_tests_from_shared(self, test_location):
        url = 'http://{0}:{1}/API/Scheduling/Explorer/Shared/{2}'.format(self.host, self.port, test_location)
        request = Request(url)
        request.get_method = lambda: 'GET'
        request.add_header('Authorization', 'Basic {}'.format(self.token))

        try:
            response = self.opener.open(request)
            result = response.read()
        except Exception as e:
            print(str(e))
            raise e

        return result


if __name__ == "__main__":
    api = QualiApi("localhost", "admin", "admin")
    tests = api.get_tests_from_shared("Demo")
    pass
