# storage
python package for simple configuration storage

this is a pre-release version and the api is subject to change.

## installation


## development

### installation
to install for development:
```
git clone ${REPO_URL} ${PATH_TO_ROOT}
pip install -e ${PATH_TO_ROOT}
```

### tests

tox is reccomended

#### tox

install tox
```pip install tox```

run tox from the root directory
```tox```

#### pytest (not reccomended)
make sure pytest is installed

run pytest from the root directory
```pytest```

## packaging

make sure the PyPA's build package is installed
```python3 -m pip install --upgrade build```

run build from the root dir
```python3 -m build```
