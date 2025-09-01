from ..diff.PgDiffUtils import PgDiffUtils

class PgView(object):
    def __init__(self, name):
        self.name = name
        self.comment = None
        self.columnNames = None
        self.defaultValues = dict()
        self.triggers=dict()
        self.columnComments = dict()
        self.query = None

    def __eq__(self, other):
        if other is None:
            return False

        if self.columnNames is None and other.columnNames is not None:
            return False
        elif self.columnNames is not None and other.columnNames is None:
            return False
        elif self.columnNames is not None and other.columnNames is not None and set(self.columnNames) != set(other.columnNames):
            return False

        if self.query.strip() != other.query.strip():
            return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def getCreationSQL(self):
        sbSQL = []
        sbSQL.append("CREATE VIEW ")
        sbSQL.append(PgDiffUtils.getQuotedName(self.name))

        if (self.columnNames is not None and len(self.columnNames) > 0):
            sbSQL.append(" (")

            sbSQL.append(','.join([PgDiffUtils.getQuotedName(columnName) for columnName in self.columnNames]))
            # for (int i = 0; i < columnNames.size(); i++) {
            #     if (i > 0) {
            #         sbSQL.append(", ");
            #     }

            #     sbSQL.append(PgDiffUtils.getQuotedName(columnNames.get(i)));
            # }
            sbSQL.append(')')

        sbSQL.append(" AS\n\t")
        sbSQL.append(self.query)
        sbSQL.append(';')

        for columnName, defaultValue in self.defaultValues.items():
            sbSQL.append("\n\nALTER VIEW ")
            sbSQL.append(PgDiffUtils.getQuotedName(self.name))
            sbSQL.append(" ALTER COLUMN ")
            sbSQL.append(PgDiffUtils.getQuotedName(columnName))
            sbSQL.append(" SET DEFAULT ")
            sbSQL.append(defaultValue)
            sbSQL.append(';')

        if self.comment:
            sbSQL.append("\n\nCOMMENT ON VIEW ")
            sbSQL.append(PgDiffUtils.getQuotedName(self.name))
            sbSQL.append(" IS ")
            sbSQL.append(self.comment)
            sbSQL.append(';')

        for columnName, columnComment in self.columnComments.items():
            if columnComment:
                sbSQL.append("\n\nCOMMENT ON COLUMN ")
                sbSQL.append(PgDiffUtils.getQuotedName(self.name))
                sbSQL.append('.')
                sbSQL.append(PgDiffUtils.getQuotedName(columnName))
                sbSQL.append(" IS ")
                sbSQL.append(columnComment)
                sbSQL.append(';')

        return ''.join(sbSQL)

    def getDropSQL(self):
        return "DROP VIEW %s;" % PgDiffUtils.getQuotedName(self.name)

    def removeColumnDefaultValue(self, columnName):
        self.defaultValues.pop(columnName, None)

    def addColumnComment(self, columnName, comment):
        self.removeColumnDefaultValue(columnName)
        self.columnComments[columnName] = comment

    def addColumnDefaultValue(self, columnName, defaultValue):
        self.defaultValues[columnName] = defaultValue

