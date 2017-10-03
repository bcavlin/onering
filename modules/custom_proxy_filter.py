from PyQt4 import QtGui


class CustomSortFilterProxyModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)
        self.filterString = ''

    def setFilterString(self, text):
        """
        text : string
            The string to be used for pattern matching.
        """
        self.filterString = text.lower()
        self.invalidateFilter()

    def filterAcceptsRow(self, row_num, parent):
        """
        Reimplemented from base class to allow the use
        of custom filtering.
        """
        model = self.sourceModel()

        last_change = str(model.data(model.index(row_num, 9)))  # this is last
        if last_change == '-1':
            return False

        if self.filterString != '':
            for column in range(model.columnCount()):
                index = model.index(row_num, column)
                result = self.filterString in str(model.data(index)).lower()
                if result:
                    return True
            return False
        else:
            return True
