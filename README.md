# nanoservices


model and transformation library for pragmatic mda approach

## Installation

```bash
pip install -r requirements.txt
```

```
pip install wheel
pip install setuptools
pip install twine```
```
```
python setup.py develop
```

## Usage

```
nano-cli --cim stuff/backup/wordpress.yml 
```

redirect to wordpress.puml and create image
```
java -jar plantuml-1.2022.6.jar wordpress.puml
```


### Test with pytest
```bash
python -m pytest tests/
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Authors and acknowledgment

- For readme file I used format from https://www.makeareadme.com/

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
