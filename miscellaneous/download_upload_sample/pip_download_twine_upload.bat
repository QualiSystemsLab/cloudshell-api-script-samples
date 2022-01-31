Rem "download package in specificed requirements file using cloudshell's python 3 interpreter from specified pypi index"
"C:\Program Files (x86)\QualiSystems\TestShell\ExecutionServer\python\3.7.1\python.exe" -m pip download -r requirements.txt --index-url https://test.pypi.org/simple/ -d dist

Rem "use separate python installation with twine installed to push to quali server local pypi"
python -m twine upload --repository-url http://localhost:8036 --skip-existing dist/* -u pypiadmin -p pypiadmin