from typing import Dict

import pytest
from src.omop_etl_wrapper.model.etl_stats import EtlStats
from src.omop_etl_wrapper.model.source_data import SourceData


@pytest.fixture
def source_data1(source_config: Dict) -> SourceData:
    """Return SourceData instance with test_dir1 as source_dir."""
    return SourceData(source_config, EtlStats())


def test_get_file_returns_the_file(source_data1: SourceData):
    file1 = source_data1.get_source_file('source_file1.csv')
    assert file1.path.name == 'source_file1.csv'


def test_get_non_existing_file_raises_exception(source_data1: SourceData):
    with pytest.raises(FileNotFoundError):
        source_data1.get_source_file('source_file99.csv')


def test_source_data_counts_are_collected(source_config: Dict):
    source_config['count_source_rows'] = True
    source_data = SourceData(source_config, EtlStats())
    assert len(source_data._etl_stats.sources) == 3


def test_source_dir_property(source_data1: SourceData):
    assert source_data1.source_dir.is_dir()
    assert source_data1.source_dir.exists()
    assert source_data1.source_dir.name == 'test_dir1'