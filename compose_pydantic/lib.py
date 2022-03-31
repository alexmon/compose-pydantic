from abc import ABC, abstractmethod

from mergedeep import merge, Strategy
from yaml import safe_load

from .models import ComposeSpecification


class ReadSpecStrategyABC(ABC):
    @abstractmethod
    def read_specs(self, arg_list: list) -> dict:
        pass


class DictSpecStrategy(ReadSpecStrategyABC):
    def read_specs(self, compose_dict_list: list) -> dict:
        """
        Reduce list of dict to a dict

        :param compose_dict_list:
        :returns:
        :raises: any of (YAMLError, ValidationError)
        """
        compose_data = {}
        for compose_dict in compose_dict_list:
            merge(compose_data, compose_dict, strategy=Strategy.REPLACE)

        return compose_data


class FileSpecStrategy(ReadSpecStrategyABC):
    def read_specs(self, compose_file_list: list) -> dict:
        """
        Read list of files adhere to Compose specification and return a dict

        :param compose_file_list: a list of values accepted by builtin function `open`
                            same key values from rightmost files will be preserved
        :returns:
        :raises: any of (OSError, YAMLError, ValidationError)
        """
        compose_data = {}
        for compose_file in compose_file_list:
            with open(compose_file, 'r') as fh:
                data = safe_load(fh)
            merge(compose_data, data, strategy=Strategy.REPLACE)

        return compose_data


class TextSpecStrategy(ReadSpecStrategyABC):
    def read_specs(self, compose_text_list: list) -> dict:
        """
        Parse list of strings adhere to Compose specification and return a dict

        :param compose_text_list:
        :returns:
        :raises: any of (YAMLError, ValidationError)
        """
        compose_data = {}
        for compose_text in compose_text_list:
            data = safe_load(compose_text)
            merge(compose_data, data, strategy=Strategy.REPLACE)

        return compose_data


class ComposeSpecificationFactory:
    def __init__(self, strategy: ReadSpecStrategyABC = None):
        self._strategy = strategy if strategy else FileSpecStrategy()

    def __call__(self, arg_list=[]) -> ComposeSpecification:
        specs_dict = self._strategy.read_specs(arg_list)
        return self._parse(specs_dict)

    @property
    def strategy(self):
        return self._strategy

    def _parse(self, compose_data: dict) -> ComposeSpecification:
        return ComposeSpecification(**compose_data)
