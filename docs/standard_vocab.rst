Standard vocabularies
=====================

.. contents::
    :local:
    :backlinks: none

.. note::
   delphyne currently only supports postgresql for loading standard vocabularies. For other dialects
   please use the instructions on the `CommonDataModel repository <https://github.com/OHDSI/CommonDataModel>`_.

Vocabulary files
----------------

All standardized data in the OMOP CDM relies on the contents of the vocabulary tables.
Loading the standard vocabularies is therefore typically one of the first steps in an ETL pipeline.
To get the vocabulary files, go to the download section of `Athena <https://athena.ohdsi.org/vocabulary/list>`_,
select the vocabularies you would like to include and click **Download Vocabularies**.

The zipped download contains the vocabulary contents as csv files, which should then be added to
the standard vocabularies folder:

::

    project_root
    └── resources
        └── vocabularies
            └── standard
                ├── CONCEPT.csv
                ├── CONCEPT_ANCESTOR.csv
                ├── CONCEPT_CLASS.csv
                ├── CONCEPT_RELATIONSHIP.csv
                ├── CONCEPT_SYNONYM.csv
                ├── DOMAIN.csv
                ├── DRUG_STRENGTH.csv
                ├── RELATIONSHIP.csv
                └── VOCABULARY.csv

Add to pipeline
---------------

Make sure the `skip_vocabulary_loading` option in your config.yml is set to False.
As part of your Wrapper's run method, the following line must be included.

.. code-block:: python

   self.vocab_manager.standard_vocabularies.load()

This will drop all indexes and constraints on the tables before insertion, and restores them afterwards.

To prevent accidental reloading of vocabularies, they can only be loaded if all the target tables are empty.
If you do want to reload them, you therefore need to drop the contents manually.
