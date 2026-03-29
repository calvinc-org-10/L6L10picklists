from datetime import date
import openpyxl
from sqlalchemy import select, and_
from models import picklist, L6L10Parts, IMSUpdate
from database import Session

class ActivePicklist:
    """View to get active picklist records where status != 'done'."""
    @staticmethod
    def get_query(session):
        return session.query(picklist).filter(picklist.status != 'done')

    @staticmethod
    def get_all(session):
        return ActivePicklist.get_query(session).all()

def importIMS(filepath):
    """
    Imports IMS spreadsheet using openpyxl, processes the data, and updates/inserts records.
    The spreadsheet contains columns: [WorkOrder, Picklist, GPN, Qty]
    """
    session = Session()
    try:
        # Empty the IMSUpdate table
        session.query(IMSUpdate).delete()
        session.commit()

        # Load workbook and read data
        # Transforms will be written by user, but mapping to IMSUpdate is typically:
        # WONumber <- WorkOrder
        # PKNumber <- Picklist
        # PartNumber <- GPN
        # remainQty <- Qty
        
        wb = openpyxl.load_workbook(filepath, data_only=True)
        sheet = wb.active
        
        # Skipping header row assuming it's the first row
        for row in sheet.iter_rows(min_row=2, values_only=True):    # type: ignore
            if not row[0]:
                continue
            
            # Assuming row = [WorkOrder, Picklist, GPN, Qty]
            wo_num = str(row[0])
            pk_num = str(row[1])
            part_num = str(row[2])
            qty = row[3]
            if qty is None:
                qty = 0
            
            new_ims = IMSUpdate(
                WONumber=wo_num,
                PKNumber=pk_num,
                PartNumber=part_num,
                remainQty=qty,
                status=None
            )
            session.add(new_ims)
        
        session.commit()

        # Update active picklists based on IMSUpdate
        active_picklists = ActivePicklist.get_all(session)
        
        for p in active_picklists:
            # Check if (PartNumber, PKNumber) is in IMSUpdate
            ims_record = session.query(IMSUpdate).filter_by(
                PartNumber=p.PartNumber, 
                PKNumber=p.PKNumber
            ).first()
            
            if ims_record:
                p.remainQty = ims_record.remainQty
                ims_record.status = "found"
            else:
                p.remainQty = 0
                p.status = "done"
                p.finishDate = date.today()
                
        session.commit()

        # Add new picklist records for items in L6L10Parts not found in IMS update
        # for each IMSUpdate record where IMSUpdate.PartNumber in L6L10Parts and IMSUpdate.status != "found"
        
        unfound_ims = session.query(IMSUpdate).filter(
            IMSUpdate.status != "found"
        ).all()
        
        for ims in unfound_ims:
            # Check if PartNumber is in L6L10Parts
            part_exists = session.query(L6L10Parts).filter_by(PartNumber=ims.PartNumber).first()
            if part_exists:
                new_picklist = picklist(
                    PartNumber=ims.PartNumber,
                    PKNumber=ims.PKNumber,
                    WONumber=ims.WONumber,
                    intQty=ims.remainQty, # Setting intQty to remainQty initially
                    remainQty=ims.remainQty,
                    status=''
                )
                session.add(new_picklist)
                
        session.commit()
                
        # Empty the IMSUpdate table after processing
        session.query(IMSUpdate).delete()
        session.commit()
        
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
