import sqlparse
import re
import logging
from ..schema.PgDatabase import PgDatabase
from ..parser.CreateSchemaParser import CreateSchemaParser
from ..parser.CreateTableParser import  CreateTableParser
from ..parser.AlterTableParser import AlterTableParser
from ..parser.CreateIndexParser import CreateIndexParser
from ..parser.CreateFunctionParser import CreateFunctionParser
from ..parser.CreateSequenceParser import CreateSequenceParser
from ..parser.AlterSequenceParser import AlterSequenceParser
from ..parser.CreateViewParser import CreateViewParser
from ..parser.CreateTriggerParser import CreateTriggerParser
from ..parser.AlterViewParser import AlterViewParser
from ..parser.CommentParser import CommentParser

class PgDumpLoader(object):

    # Pattern for testing whether it is CREATE SCHEMA statement.
    PATTERN_CREATE_SCHEMA = re.compile(r"^CREATE[\s]+SCHEMA[\s]+.*$", re.I | re.S)
    # Pattern for parsing default schema (search_path).
    PATTERN_DEFAULT_SCHEMA = re.compile(r"^SET[\s]+search_path[\s]*=[\s]*\"?([^,\s\"]+)\"?(?:,[\s]+.*)?;$", re.I | re.S)
    # Pattern for testing whether it is CREATE TABLE statement.
    PATTERN_CREATE_TABLE = re.compile("^CREATE[\s]+TABLE[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is CREATE VIEW statement.
    PATTERN_CREATE_VIEW = re.compile("^CREATE[\s]+(?:OR[\s]+REPLACE[\s]+)?VIEW[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is ALTER TABLE statement.
    PATTERN_ALTER_TABLE = re.compile("^ALTER[\s]+TABLE[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is CREATE SEQUENCE statement.
    PATTERN_CREATE_SEQUENCE = re.compile("^CREATE[\s]+SEQUENCE[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is ALTER SEQUENCE statement.
    PATTERN_ALTER_SEQUENCE =re.compile("^ALTER[\s]+SEQUENCE[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is CREATE INDEX statement.
    PATTERN_CREATE_INDEX = re.compile("^CREATE[\s]+(?:UNIQUE[\s]+)?INDEX[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is SELECT statement.
    PATTERN_SELECT = re.compile("^SELECT[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is INSERT INTO statement.
    PATTERN_INSERT_INTO = re.compile("^INSERT[\s]+INTO[\\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is UPDATE statement.
    PATTERN_UPDATE = re.compile("^UPDATE[\s].*$", re.I | re.S)
    # Pattern for testing whether it is DELETE FROM statement.
    PATTERN_DELETE_FROM = re.compile("^DELETE[\s]+FROM[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is CREATE TRIGGER statement.
    PATTERN_CREATE_TRIGGER = re.compile("^CREATE[\s]+TRIGGER[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is CREATE FUNCTION or CREATE OR REPLACE FUNCTION statement.
    PATTERN_CREATE_FUNCTION = re.compile("^CREATE[\s]+(?:OR[\s]+REPLACE[\s]+)?FUNCTION[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is ALTER VIEW statement.
    PATTERN_ALTER_VIEW = re.compile("^ALTER[\s]+VIEW[\s]+.*$", re.I | re.S)
    # Pattern for testing whether it is COMMENT statement.
    PATTERN_COMMENT = re.compile("^COMMENT[\s]+ON[\s]+.*$", re.I | re.S)

    @staticmethod
    def loadDatabaseSchema(dumpFileName, ignoreSlonyTriggers = False):
        database = PgDatabase()
        logging.debug('Loading %s file' % dumpFileName)

        statements = sqlparse.split(open(dumpFileName,'r'))
        logging.debug('Parsed %d statements' % len(statements))

        create_schema_statements = []
        create_table_statements = []
        alter_table_statements = []
        create_index_statements = []
        create_trigger_statements = []
        create_function_statements = []
        create_sequence_statements = []
        alter_sequence_statements = []
        create_view_statements = []
        alter_view_statements = []
        comment_statements = []
        other_statements = []

        for statement in statements:
            statement = PgDumpLoader.strip_comment(statement).strip()
            if not statement:
                continue

            if PgDumpLoader.PATTERN_CREATE_SCHEMA.match(statement):
                create_schema_statements.append(statement)
            elif PgDumpLoader.PATTERN_DEFAULT_SCHEMA.match(statement):
                # Default schema needs to be set early
                match = PgDumpLoader.PATTERN_DEFAULT_SCHEMA.match(statement)
                database.setDefaultSchema(match.group(1))
            elif PgDumpLoader.PATTERN_CREATE_TABLE.match(statement):
                create_table_statements.append(statement)
            elif PgDumpLoader.PATTERN_ALTER_TABLE.match(statement):
                alter_table_statements.append(statement)
            elif PgDumpLoader.PATTERN_CREATE_SEQUENCE.match(statement):
                create_sequence_statements.append(statement)
            elif PgDumpLoader.PATTERN_ALTER_SEQUENCE.match(statement):
                alter_sequence_statements.append(statement)
            elif PgDumpLoader.PATTERN_CREATE_INDEX.match(statement):
                create_index_statements.append(statement)
            elif PgDumpLoader.PATTERN_CREATE_VIEW.match(statement):
                create_view_statements.append(statement)
            elif PgDumpLoader.PATTERN_ALTER_VIEW.match(statement):
                alter_view_statements.append(statement)
            elif PgDumpLoader.PATTERN_CREATE_TRIGGER.match(statement):
                create_trigger_statements.append(statement)
            elif PgDumpLoader.PATTERN_CREATE_FUNCTION.match(statement):
                create_function_statements.append(statement)
            elif PgDumpLoader.PATTERN_COMMENT.match(statement):
                comment_statements.append(statement)
            else:
                other_statements.append(statement)

        for statement in create_schema_statements:
            CreateSchemaParser.parse(database, statement)
        for statement in create_table_statements:
            CreateTableParser.parse(database, statement)
        for statement in alter_table_statements:
            AlterTableParser.parse(database, statement)
        for statement in create_sequence_statements:
            CreateSequenceParser.parse(database, statement)
        for statement in alter_sequence_statements:
            AlterSequenceParser.parse(database, statement)
        for statement in create_index_statements:
            CreateIndexParser.parse(database, statement)
        for statement in create_view_statements:
            CreateViewParser.parse(database, statement)
        for statement in alter_view_statements:
            AlterViewParser.parse(database, statement)
        for statement in create_trigger_statements:
            CreateTriggerParser.parse(database, statement, ignoreSlonyTriggers)
        for statement in create_function_statements:
            CreateFunctionParser.parse(database, statement)
        for statement in comment_statements:
            CommentParser.parse(database, statement)

        for statement in other_statements:
            logging.info('Ignored statement: %s' % statement)

        return database


    @staticmethod
    def strip_comment(statement):
        start = statement.find("--")

        while start >= 0:
            end = statement.find("\n", start)
            if start < end:
                statement = statement[end:]
            else:
                statement = statement[:start]

            start = statement.find("--")

        return statement
