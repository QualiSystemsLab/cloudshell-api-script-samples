from quali_utils.quali_packaging import PackageEditor
import sys


def _flat_heirarchy(self, *args):
    strArgs = []
    for i, s in enumerate(args):
        if isinstance(s, list):
            strArgs.extend(self._flat_heirarchy(self, *tuple(s)))
        elif isinstance(s, tuple):
            strArgs.extend(self._flat_heirarchy(self, *s))
        elif isinstance(s, type(self)):
            pass
        elif sys.version_info[0] >= 3:
            if isinstance(s, str):
                strArgs.append('"{}"'.format(s))
        else:
            strArgs.append('"'+str(s).encode('UTF-8')+'"')
    return strArgs


PACKAGE_PATH = r"C:\Users\natti.k\code\quali\cloudshell-api-script-samples\packaging-api-samples\quote bug test.zip"

p = PackageEditor()
p.process._flat_heirarchy = _flat_heirarchy
p.load(PACKAGE_PATH)
x = p.change_topology_name_and_alias("quote bug test", "lolll")
names = p.get_topology_names()
topology_name = p.get_topology_names()[0]
apps = p.get_apps(topology_name)
app1 = apps[0]
app1_name = app1.appResource.name

p.edit_app(topology_name=topology_name, app_name=app1_name, topology_app=app1)
