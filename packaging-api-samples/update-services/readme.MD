# Update VLAN Services
This script is utility script to update VLAN ID attribute on services in existing blueprints


### Usage
- install all dependencies in requirements.txt (note that quali-utils packaging api is hosted in download center)
- add credentials to credentials.py
- Run cli.py, passing in target VLAN service, existing vlan id, and the new desired vlan id

Sample Command
```commandline
python .\cli.py "VLAN Manual" 129 169
```

Sample output
```commandline
Starting Flow. Changing service 'VLAN Manual' VLAN 129 --> 169
starting blueprint search
System Blueprint Count: 148
found target blueprint vlan dev
Target blueprints found: 1
search done after 17 seconds
processing blueprint vlan dev
['C:\\Users\\natti.k\\code\\quali\\venvs\\cloudshell-api-script-samples\\PY39_cloudshell\\lib\\site-packages\\quali_utils\\QualiSystems.Packaging.exe', 'GetTopologyNames', '--packagepath', 'vlan dev.zip']
['C:\\Users\\natti.k\\code\\quali\\venvs\\cloudshell-api-script-samples\\PY39_cloudshell\\lib\\site-packages\\quali_utils\\QualiSystems.Packaging.exe', 'SetAttributeToService', '--packagepath', 'vlan dev.zip', '--topologyna
me', 'vlan dev', '--servicealias', 'VLAN Manual', '--attributename', 'VLAN ID', '--attributevalue', '169', '--publish', 'False']
done processing vlan dev after 5 seconds
Update flow done after total 23 seconds
```


### Implementation Details
This script uses the following flow:
- automation api to search system for target blueprints
- quali REST api to download target blueprint packages
- cleans package of everything except topologies folder to optimize the import request
- packaging api updates target attribute
- Quali REST api loads package back into server