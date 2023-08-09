
import yaml
import codecs

class YamlLoadError(Exception):
    pass

def YamlToDict(filename: str):
    with codecs.open(filename, 'r', 'utf-8') as f:
        try:
            data = yaml.safe_load(f)
            return data
        except Exception as e:
            raise YamlLoadError(e)

