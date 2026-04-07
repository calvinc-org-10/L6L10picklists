from typing import Any

from PySide6.QtWidgets import (
    QLineEdit, QDateEdit,
    QPushButton, 
    QVBoxLayout,
    )

from models import picklist, L6L10Parts
from database import get_app_sessionmaker

from calvincTools.utils import (
    get_primary_key_column,
    cDataList,
    )
from calvincTools.database import Repository
from calvincTools.utils.forms import (
    cQFmConstants,
    cQFormFieldDef, cQFormBtnDef,
    cSRFSingleRecordForm,
    cSRFMultiRecordWrapper,
    cSRFRecordGrid, cSRFRecordList, cSRFRecordList_Record,
)

partnum_choices = {r.PartNumber: str(r.PartNumber) for r in Repository(get_app_sessionmaker(), L6L10Parts).get_all()}

class picklist_record(cSRFRecordList_Record):
    """
    Form to edit a single picklist record. Inherits from calvincTools.cSRFSingleRecordForm.
    """
    _ORMmodel = picklist
    _primary_key = get_primary_key_column(picklist)
    _ssnmaker = get_app_sessionmaker()

    # def __init__(self, record: Any, parent=None):
    #     super().__init__(record=record, parent=parent)
    
    def defineFields(self):
        r = [
            cQFormFieldDef(name='status',
                label='Status',
                widget_type=QLineEdit,
                position=(0, 0, 1, 2),
            ),
            cQFormFieldDef(name='priority',
                label='Priority',
                widget_type=QLineEdit,
                position=(0, 2),
            ),
            cQFormFieldDef(name='PartNumber',
                label='Part Number',
                widget_type=cDataList,
                choices=partnum_choices,
                position=(0, 3, 1,  2),
            ),
            cQFormFieldDef(name='PKNumber',
                label='PK Number',
                widget_type=QLineEdit,
                position=(1, 0, 1, 2),
            ),
            cQFormFieldDef(name='Requestor',
                label='Requestor',
                widget_type=QLineEdit,
                position=(1, 2, 1, 2),
            ),
            cQFormFieldDef(name='WONumber',
                label='WO Number',
                widget_type=QLineEdit,
                position=(1, 3),
            ),
            cQFormFieldDef(name='intQty',
                label='Initial Qty',
                widget_type=QLineEdit,
                position=(1, 5),
            ),
            cQFormFieldDef(name='remainQty',
                label='Remain Qty',
                widget_type=QLineEdit,
                position=(1, 6),
            ),
            cQFormFieldDef(name='salesOrder',
                label='Sales Order',
                widget_type=QLineEdit,
                position=(0, 4),
            ),
            cQFormFieldDef(name='owner',
                label='Owner',
                widget_type=QLineEdit,
                position=(0, 5),
            ),
            cQFormFieldDef(name='finishDate',
                label='Finish Date',
                widget_type=QDateEdit,
                position=(0, 6),
            ),
            cQFormFieldDef(name='notes',
                label='Notes',
                widget_type=QLineEdit,
                position=(2, 1, 1, 6),
            ),
        ]
        return r

class lstPicklist_records(cSRFRecordList):
    """
    Form to list picklist records. Inherits from calvincTools.cSRFRecordList.
    """
    _ORMmodel = picklist
    _primary_key = get_primary_key_column(picklist)
    _ssnmaker = get_app_sessionmaker()
    _recordClass = picklist_record
    _page_spacing = 2
    
    def defineFields(self):
        return []
    
class editPicklist(cSRFMultiRecordWrapper):
    """
    Main form to edit picklist records, with subforms for different views.
    Inherits from calvincTools.cSRFMultiRecordWrapper.
    """
    _formname = "Edit Picklists"

    def defineFields(self):
        r = [
            cQFormFieldDef(name='ToggleActive',
                field_type=cQFormFieldDef.cQFormFieldType.INTERNAL,
                label='Toggle Active',
                widget_type=QPushButton,
                page=cQFmConstants.pageFixedTop,
                position=(0, 2),
            ),
            cQFormFieldDef(name='Picklists',
                field_type=cQFormFieldDef.cQFormFieldType.SUBFORM,
                widget_type=lstPicklist_records,
                label='All Picklists',
                position=(0, 0, 4, 1),
            ),
        ]
        return r

class editPicklist_v0(cSRFSingleRecordForm):
    #### AI generated code - may require adjustments to fit calvincTools API and form layout. Please review and modify as needed. ####
    """
    Form to edit picklist records. Inherits from calvincTools.cSRFSingleRecordForm.
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
        # depending on the actual layout structure of cSRFSingleRecordForm
        if self.layout() is not None:
            self.layout().insertWidget(0, self.btn_active_filter)       #type: ignore
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
                self.set_filter(picklist.status != 'done')  # type: ignore
            else:
                print("calvincTools.cSRFSingleRecordForm does not have set_filter. Filter not applied.")
        else:
            # Clear the filter
            if hasattr(self, 'clear_filter'):
                self.clear_filter() #type: ignore
            elif hasattr(self, 'set_filter'):
                self.set_filter(None)   #type: ignore

class editL6L10PartsSub(cSRFRecordGrid):
    """
    Form to edit L6L10Parts records. 
    """
    _ORMmodel = L6L10Parts
    _primary_key = get_primary_key_column(L6L10Parts)
    _ssnmaker = get_app_sessionmaker()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
# editL6L10PartsSub
class editL6L10PartsMain(cSRFMultiRecordWrapper):
    """
    Main form to edit L6L10Parts records, with subforms for different views.
    Inherits from calvincTools.cSRFMultiRecordWrapper.
    """
    _formname = "Edit L6L10Parts"

    def defineFields(self):
        r = [
            cQFormFieldDef(name='L6L10Parts',
                field_type=cQFormFieldDef.cQFormFieldType.SUBFORM,
                widget_type=editL6L10PartsSub,
                label='L6 to L10 Parts',
                position=(0, 0),
            ),
        ]
        return r
    # defineFields
# editL6L10PartsMain
            