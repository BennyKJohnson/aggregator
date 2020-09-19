import os

from pyhocon import ConfigFactory


class Config(object):
    """
    Main config entry point. Provides convenient interface to
    configuration information stored in aggregator.conf file.
    Each section in config file has it's own class, that should be defined here.
    """

    def __init__(self, config_file_path=None):
        if config_file_path is None:
            if "AGGREGATOR__CONFIG_FILE_PATH" in os.environ:
                config_file_path = os.environ["AGGREGATOR__CONFIG_FILE_PATH"]
            else:
                config_file_path = "aggregator.conf"

        config = ConfigFactory.parse_file(config_file_path)

        self.data = DataConfig(config)
        self.persistence = PersistenceConfig(config)
        self.feeder = FeederConfig(config)
        self.tasks = TasksConfig(config)


class DataConfig(object):
    def __init__(self, config):
        self.dir = config.get("data.dir")
        self.out_dir = config.get("data.out.dir")


class PersistenceConfig(object):
    def __init__(self, config):
        self.migrations = MigrationsConfig(config)
        self.credentials_file_path = config.get("persistence.credentials_file_path")


class MigrationsConfig(object):
    def __init__(self, config):
        self.migrations_dir = config.get("persistence.migrations.migrations_dir")


class FeederConfig(object):
    def __init__(self, config):
        self.timeout_seconds = config.get("feeder.timeout_seconds")


class TasksConfig(object):
    def __init__(self, config):
        self.import_feeds = ImportFeedsTaskConfig(config)


class ImportFeedsTaskConfig(object):
    def __init__(self, config):
        self.truncate = config.get("tasks.import_feeds.truncate")
        self.feeds_file_path = config.get("tasks.import_feeds.feeds_file_path")
