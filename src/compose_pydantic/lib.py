from abc import ABC, abstractmethod
from os import PathLike
from typing import Any, Union

from mergedeep import merge, Strategy
from yaml import safe_load

from .models import ComposeSpecification


StrOrBytesPath = Union[str, bytes, PathLike[str], PathLike[bytes]]


class ReadSpecStrategyABC(ABC):
    @abstractmethod
    def read_specs(self, source: Any, overrides: list) -> dict:
        pass


class DictSpecStrategy(ReadSpecStrategyABC):
    def read_specs(self, source: dict, overrides: list[dict]) -> dict:
        """
        Work on dict represantations

        :raises: any of (YAMLError, ValidationError)
        """
        compose_data = source
        for compose_dict in overrides:
            merge(compose_data, compose_dict, strategy=Strategy.REPLACE)

        return compose_data


class FileSpecStrategy(ReadSpecStrategyABC):
    def read_specs(self, source: StrOrBytesPath, overrides: list[StrOrBytesPath]) -> dict:
        """
        Read list of files adhere to Compose specification and return a dict

        :param source:
        :param overrides: a list of values accepted by builtin function `open`
                            same key values from rightmost files will be preserved
        :raises: any of (OSError, YAMLError, ValidationError)
        """
        with open(source, 'r') as fh:
            compose_data = safe_load(fh)
        for compose_file in overrides:
            with open(compose_file, 'r') as fh:
                data = safe_load(fh)
            merge(compose_data, data, strategy=Strategy.REPLACE)

        return compose_data


class TextSpecStrategy(ReadSpecStrategyABC):
    def read_specs(self, source: str, overrides: list[str]) -> dict:
        """
        Parse list of strings adhere to Compose specification and return a dict

        :raises: any of (YAMLError, ValidationError)
        """
        compose_data = safe_load(source)
        for compose_text in overrides:
            data = safe_load(compose_text)
            merge(compose_data, data, strategy=Strategy.REPLACE)

        return compose_data


class ComposeSpecificationFactory:
    def __init__(self, strategy: ReadSpecStrategyABC = None):
        self._strategy = strategy if strategy else FileSpecStrategy()

    def __call__(self, source, overrides=[]) -> ComposeSpecification:
        specs_dict = self._strategy.read_specs(source, overrides)
        return self._parse(specs_dict)

    @property
    def strategy(self):
        return self._strategy

    def _parse(self, compose_data: dict) -> ComposeSpecification:
        return ComposeSpecification(**compose_data)
