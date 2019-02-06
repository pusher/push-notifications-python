# Release a new Push Notifications Python version
## Requirements
- Python
- Twine (`pip install twine`)
- wheel (`pip install wheel`)
- .pypirc
### pypirc
Create a `.pypirc` file in your home directory:
```
[pypi]
username = Pusher
password = <password is in LastPass>
```

## Steps
### Create release commit
 - Update all references to old version (e.g. in setup.py)
 - Update Changelog
 - Commit changes with message "Bump version to x.y.z"
 - Push changes
 - Create Github release
### Build package
```
$ python setup.py sdist bdist_wheel
```
### Upload to test PyPi
```
$ twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```
(Then check that this worked at https://test.pypi.org/project/pusher-push-notifications/)

### Upload to production PyPi
```
$ twine upload ./dist/*
```
