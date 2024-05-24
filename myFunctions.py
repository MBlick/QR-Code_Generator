
import configparser

# function to extract the url
def extractURL(filePath, extension):
    if extension == '.url':
        config = configparser.RawConfigParser()
        try:
            config.read(filePath)
            # try "InternetShortcut" section first (common format)
            if config.has_section('InternetShortcut'):
                return config.get('InternetShortcut', 'URL')
            # fallback to "DEFAULT" section for extended formats
            elif config.has_section('DEFAULT'):
                return config.get('DEFAULT', 'BASEURL')
            else:
                return None  # URL not found in either section
        except (configparser.Error, FileNotFoundError) as e:
            print(f"Error reading shortcut file: {e}")
            return None
    if extension == '.txt':
        # open the file in read mode and extract the text
        with open(filePath, 'r', encoding='utf-8', errors='ignore') as f:  
            data = f.read()
        return data