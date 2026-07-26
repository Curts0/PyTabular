"""Small TOM-like objects used by offline unit tests."""

from __future__ import annotations

from dataclasses import dataclass, field


class Collection(list):
    """List with the TOM ``Add`` spelling."""

    def Add(self, value: object) -> None:
        self.append(value)


@dataclass
class FakeTable:
    Name: str
    Partitions: Collection = field(default_factory=Collection)
    Columns: Collection = field(default_factory=Collection)
    Measures: Collection = field(default_factory=Collection)


@dataclass
class FakeModel:
    Name: str = "Model"
    Tables: Collection = field(default_factory=Collection)
    Relationships: Collection = field(default_factory=Collection)
    Cultures: Collection = field(default_factory=Collection)
    Expressions: Collection = field(default_factory=Collection)
    DataSources: Collection = field(default_factory=Collection)
    Functions: Collection = field(default_factory=Collection)
    validation: Collection = field(default_factory=Collection)

    def Validate(self) -> Collection:
        return self.validation


@dataclass
class FakeDatabase:
    Model: FakeModel = field(default_factory=FakeModel)
    CompatibilityLevel: int = 1600
    Name: str = "Test"
