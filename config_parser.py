def get_config() -> dict:
    _config = dict()
    with open("config.ini", "r") as config_file:
        config_type: str = "unnamed"
        for line in config_file.readlines():
            line = line.replace("\n", "")
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                config_type = line[1:-1]
                _config.update({config_type: {}})
            else:
                name, value = line.split("=")[0], line.split("=")[1]
                _config[config_type].update({name: value})

    _config["GLOBAL"]["debug"] = True if _config["GLOBAL"]["debug"] == "1" else False
    return _config
