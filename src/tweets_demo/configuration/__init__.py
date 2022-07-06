import os
import sys

from config import ConfigurationSet, config_from_yaml, config_from_env
from tweets_demo import ROOT_PATH

PREFIX = "tweets_demo"


def config():
    env = os.environ.get("env", "local")
    return ConfigurationSet(
        config_from_env(prefix=PREFIX),
        config_from_yaml(f"{ROOT_PATH}/src/tweets_demo/configuration/{env}.yml", read_from_file=True),
    )
