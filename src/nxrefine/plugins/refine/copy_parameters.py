from nexpy.gui.datadialogs import BaseDialog
from nexpy.gui.utils import report_error
from nexusformat.nexus import NeXusError
from nxrefine.nxreduce import NXReduce


def show_dialog():
    try:
        dialog = CopyDialog()
        dialog.show()
    except NeXusError as error:
        report_error("Copying Parameters", error)


class CopyDialog(BaseDialog):

    def __init__(self, parent=None):
        super(CopyDialog, self).__init__(parent)

        self.select_root(self.choose_root, text='Select Output File')
        self.set_layout(self.root_layout,
                        self.checkboxes(('overwrite', 'Overwrite', True)),
                        self.close_buttons(save=True))
        self.checkbox['overwrite'].setVisible(False)
        self.set_title('Copying Parameters')
        self._selected = False

    def choose_root(self):
        self.checkbox['overwrite'].setVisible(False)
        for entry in [e for e in self.root if e != 'entry']:
            reduce = NXReduce(self.root[entry])
            if not reduce.not_complete('nxcopy'):
                self.checkbox['overwrite'].setVisible(True)
        self._selected = True

    @property
    def overwrite(self):
        return (self.checkbox['overwrite'].isChecked() or
                not self.checkbox['overwrite'].isVisible)

    def accept(self):
        if not self._selected:
            raise NeXusError("Need to select output file before saving")
        elif self.root.nxfilemode == 'r':
            raise NeXusError("NeXus file is locked")
        if self.overwrite:
            for entry in [e for e in self.root if e != 'entry']:
                reduce = NXReduce(self.root[entry], copy=True, overwrite=True)
                reduce.nxcopy()
        else:
            raise NeXusError("Much check 'overwrite' to save parameters")
        super(CopyDialog, self).accept()
