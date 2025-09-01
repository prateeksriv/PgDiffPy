import argparse
import logging
from . import PgDiff
from .helpers.Writer import Writer
from .loaders.PgDumpLoader import PgDumpLoader
from .diff.PgDiffUtils import PgDiffUtils
from .SearchPathHelper import SearchPathHelper
from .diff.PgDiffTables import PgDiffTables
from .diff.PgDiffTriggers import PgDiffTriggers
from .diff.PgDiffViews import PgDiffViews
from .diff.PgDiffConstraints import PgDiffConstraints
from .diff.PgDiffIndexes import PgDiffIndexes
from .diff.PgDiffSequences import PgDiffSequences
from .diff.PgDiffFunctions import PgDiffFunctions


class LogLevelAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if values == 'DEBUG':
            setattr(namespace, self.dest, logging.DEBUG)
        elif values == 'INFO':
            setattr(namespace, self.dest, logging.INFO)
        elif values == 'WARNING':
            setattr(namespace, self.dest, logging.WARNING)
        elif values == 'ERROR':
            setattr(namespace, self.dest, logging.ERROR)
        elif values == 'CRITICAL':
            setattr(namespace, self.dest, logging.CRITICAL)


def main():
    parser = argparse.ArgumentParser(prog='PgDiffPy', usage='python PgDiff.py [options] <old_dump> <new_dump>')

    parser.add_argument('old_dump')
    parser.add_argument('new_dump')

    parser.add_argument('--add-transaction', dest='addTransaction', action='store_true',
                        help="Adds START TRANSACTION and COMMIT TRANSACTION to the generated diff file")
    parser.add_argument('--add-defaults', dest='addDefaults', action='store_true',
                        help=("adds DEFAULT ... in case new column has NOT NULL constraint but no default value "
                              "(the default value is dropped later)"))
    parser.add_argument('--ignore-start-with', dest='ignoreStartWith', action='store_false',
                        help="ignores START WITH modifications on SEQUENCEs (default is not to ignore these changes)")
    parser.add_argument('--ignore-function-whitespace', dest='ignoreFunctionWhitespace', action='store_true',
                        help="ignores multiple spaces and new lines when comparing content of functions\n\                              \t- WARNING: this may cause functions to appear to be same in cases they are\n\                              \tnot, so use this feature only if you know what you are doing")

    parser.add_argument('--loglevel', dest='loglevel', action=LogLevelAction
                        , choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
                        , default=logging.ERROR, help="")

    arguments = parser.parse_args()
    logging.basicConfig(format=u'%(filename)s:%(lineno)d [%(levelname)s] %(message)s'
                        , level=arguments.loglevel)

    writer = Writer()

    try:
        PgDiff.create_diff(writer, arguments)
        print(writer)
    except Exception as e:
        if arguments.loglevel == logging.DEBUG:
            import sys
            import traceback
            traceback.print_exception(*sys.exc_info())
        else:
            print('Error: %s' % e)
        exit(1)

if __name__ == "__main__":
    main()
