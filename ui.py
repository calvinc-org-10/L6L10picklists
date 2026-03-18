from PySide6.QtWidgets import QPushButton, QVBoxLayout
from models import picklist, L6L10Parts
from database import get_app_sessionmaker

from calvincTools.utils import (
    cSimpleMultiRecordSubFmWrapperForm,
    cSimpleRecordForm, 
    cSimpleRecordSubForm1, cSimpleRecordSubForm2,
    )

class editPicklist(cSimpleRecordForm):
    """
    Form to edit picklist records. Inherits from calvincTools.cSimpleRecordForm.
    Includes a button/mechanism to restrict view to ActivePicklist.
    """
    def __init__(self, parent=None):
        # Initialize with the picklist model
        super().__init__(model=picklist, parent=parent)
        
        # Add a button to toggle ActivePicklist view
        self.btn_active_filter = QPushButton("Show Active Picklists Only")
        self.btn_active_filter.setCheckable(True)
        self.btn_active_filter.toggled.connect(self.on_active_filter_toggled)
        
        # Attempt to add to form layout if one exists; user may need to adjust
        # depending on the actual layout structure of cSimpleRecordForm
        if self.layout() is not None:
            self.layout().insertWidget(0, self.btn_active_filter)
        else:
            layout = QVBoxLayout(self)
            layout.addWidget(self.btn_active_filter)

    def on_active_filter_toggled(self, checked):
        """
        Applies a filter to the form to only show active picklists.
        The exact implementation method (e.g., set_filter) depends on calvincTools API.
        """
        if checked:
            # Show only records where status != 'done'
            if hasattr(self, 'set_filter'):
                self.set_filter(picklist.status != 'done')
            else:
                print("calvincTools.cSimpleRecordForm does not have set_filter. Filter not applied.")
        else:
            # Clear the filter
            if hasattr(self, 'clear_filter'):
                self.clear_filter()
            elif hasattr(self, 'set_filter'):
                self.set_filter(None)

class editL6L10PartsSub(cSimpleRecordSubForm1):
    """
    Form to edit L6L10Parts records. Inherits from calvincTools.cSimpleTableForm.
    """
    def __init__(self, parent=None):
        # Initialize with the L6L10Parts model
        super().__init__(
            formname='L6 to L10 Parts', 
            tbl=L6L10Parts, 
            ssnmaker=get_app_sessionmaker(),
            parent=parent
            )
class editL6L10PartsMain(cSimpleMultiRecordSubFmWrapperForm):
    """
    Main form to edit L6L10Parts records, with subforms for different views.
    Inherits from calvincTools.cSimpleMultiRecordSubFmWrapperForm.
    """
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        # Create subforms for different views of L6L10Parts
        self.subform_all = editL6L10Parts(parent=self)
        self.subform_active = editL6L10Parts(parent=self)
        self.subform_active.btn_active_filter.setChecked(True)  # Set to show active by default
        
        # Add subforms to the wrapper form
        self.add_subform(self.subform_all, "All L6L10 Parts")
        self.add_subform(self.subform_active, "Active L6L10 Parts")