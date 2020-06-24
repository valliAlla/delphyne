import pytest
from sqlalchemy import inspect
from src.omop_etl_wrapper.database.database import Database
from src.omop_etl_wrapper import Wrapper


@pytest.mark.usefixtures("container")
def test_db_does_not_exist(db_config, caplog):
    uri = f'postgresql://postgres:secret@localhost:{db_config.port}/foobar'
    assert not Database.can_connect(uri)
    assert 'Database "foobar" does not exist' in caplog.text


@pytest.mark.usefixtures("container")
def test_connection_invalid(caplog):
    uri = f'postgresql://postgres:secret@localhost:123456/postgres'
    assert not Database.can_connect(uri)
    assert 'Database "postgres" does not exist' not in caplog.text


@pytest.mark.usefixtures("test_db")
def test_db_exists():
    uri = f'postgresql://postgres:secret@localhost:7722/test_db'
    assert Database.can_connect(uri)


@pytest.mark.usefixtures("test_db")
def test_create_schemas(wrapper_cdm531: Wrapper):
    schemas = inspect(wrapper_cdm531.db.engine).get_schema_names()
    assert set(schemas) == {'information_schema', 'public'}
    wrapper_cdm531.create_schemas()
    schemas = inspect(wrapper_cdm531.db.engine).get_schema_names()
    assert set(schemas) == {'information_schema', 'public', 'cdm', 'vocab'}


@pytest.mark.usefixtures("test_db")
def test_create_tables_cdm531(wrapper_cdm531: Wrapper):
    wrapper_cdm531.create_schemas()
    wrapper_cdm531.create_cdm()
    vocab_tables = inspect(wrapper_cdm531.db.engine).get_table_names('vocab')
    assert set(vocab_tables) == {
        'domain', 'concept_ancestor', 'drug_strength', 'concept_relationship', 'vocabulary',
        'concept_synonym', 'relationship', 'concept_class', 'source_to_concept_map',
        'concept', 'cohort_definition'}
    cdm_tables = inspect(wrapper_cdm531.db.engine).get_table_names('cdm')
    assert set(cdm_tables) == {
        'cdm_source', 'device_exposure', 'condition_occurrence', 'metadata',
        'fact_relationship', 'drug_exposure', 'measurement', 'death', 'note', 'note_nlp',
        'observation', 'procedure_occurrence', 'observation_period', 'visit_occurrence',
        'specimen', 'cohort', 'visit_detail', 'condition_era', 'payer_plan_period',
        'provider', 'care_site', 'location', 'cost', 'stem_table', 'person', 'drug_era',
        'dose_era'}


@pytest.mark.skip('Needs separate process')
@pytest.mark.usefixtures("test_db")
def test_create_tables_cdm600(wrapper_cdm600: Wrapper):
    wrapper_cdm600.create_schemas()
    wrapper_cdm600.create_cdm()
    vocab_tables = inspect(wrapper_cdm600.db.engine).get_table_names('vocab')
    assert set(vocab_tables) == {}
    cdm_tables = inspect(wrapper_cdm600.db.engine).get_table_names('cdm')
    assert set(cdm_tables) == {}