from PyQt4 import QtGui, QtCore


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
            filters_ = [x.strip() for x in self.filterString.split(";")]
            found = [False] * len(filters_)
            for idx, filter_ in enumerate(filters_):
                for column in range(model.columnCount()):
                    index = model.index(row_num, column)
                    value = str(model.data(index)).lower()
                    if filter_ in value:
                        found[idx] = True

            return all(found)
        else:
            return True

    def data(self, QModelIndex, role=None):
        if role == QtCore.Qt.ToolTipRole:
            model = self.sourceModel()
            data = []
            for column in range(model.columnCount()):
                index = model.index(QModelIndex.row(), column)
                data.append(str(model.data(index)))
            return 'Tooltip: ' + str(data)
        else:
            return super().data(QModelIndex, role)
