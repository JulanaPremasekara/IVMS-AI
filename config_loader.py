import yaml
import os

def load_config(config_path='config.yaml'):
    """
    Load configuration from YAML file.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration dictionary.

    Raises:
        FileNotFoundError: If config file doesn't exist.
        yaml.YAMLError: If YAML parsing fails.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")

    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config

def get_config_value(config, key_path, default=None):
    """
    Safely get a value from nested config dictionary.

    Args:
        config (dict): Configuration dictionary.
        key_path (str): Dot-separated path to the key (e.g., 'model.max_iter').
        default: Default value if key is missing.

    Returns:
        Value from config or default.

    Raises:
        KeyError: If key is missing and no default provided.
    """
    keys = key_path.split('.')
    value = config

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            if default is not None:
                return default
            else:
                raise KeyError(f"Configuration key '{key_path}' not found.")

    return value