from configparser import ConfigParser

#load DB configuration from file (default database.ini)
def load_config(file='../database.ini',  section='postgresql'):
    parser = ConfigParser()
    parser.read(file)

    config =  {}

    if parser.has_section(section):
        data = parser.items(section)
        for d in data:
            config[d[0]] = d[1]

    else:
        raise Exception('{0} is not a valid section in {1}'.format(section, file))
    
    return config


if __name__ == '__main__':
    config  = load_config()
    print(config)