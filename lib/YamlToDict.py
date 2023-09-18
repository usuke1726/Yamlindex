
import yaml
import codecs

class YamlLoadError(Exception):
    pass

def YamlToDictList(filename: str):
    with codecs.open(filename, 'r', 'utf-8') as f:
        try:
            data = [d for d in yaml.safe_load_all(f) if not d is None]
            return data
        except Exception as e:
            raise YamlLoadError(e)

