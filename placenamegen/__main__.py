import argparse
import importlib

from placenamegen.config import Config
from placenamegen.generate import generate_place_name


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-c', '--config', type=str, default='nsw', help='Place config to use')
    arg_parser.add_argument('-n', '--count', type=int, default=1, help='Number of unique place names to generate')

    args = arg_parser.parse_args()
    config_name: str = args.config
    name_count: int = args.count

    config_module = importlib.import_module(f'placenamegen.config.data.{config_name}')
    config: Config = config_module.get_config()

    names: set[str] = set()
    while len(names) < name_count:
        name = generate_place_name(config)
        if name not in names:
            print(name)
            names.add(name)
