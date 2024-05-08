from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

BasePO = declarative_base()
class POEntity(BasePO):
    __table_args__ = {'schema': 'dbo'} 
    __tablename__ = 'PO'
    
    POId            = Column(String, primary_key=True)
    PONumber        = Column(String)
    PODate          = Column(DateTime)
    StoreNo         = Column(Integer)
    ShipDate        = Column(DateTime)
    CancelDate      = Column(DateTime)
    CreationDate    = Column(DateTime)
    VendorCode      = Column(String)
    StatusCode      = Column(String)
    Buyer           = Column(String)
    CostTotal       = Column(Float)
    RetailTotal     = Column(Float)
    RetailTotalWTax = Column(Float)
    
BasePOLine = declarative_base()
class POLineEntity(BasePOLine):
    __table_args__ = {'schema': 'dbo'} 
    __tablename__ = 'PO_LINE'
    
    POId            = Column(String, primary_key=True)
    LineId          = Column(String, primary_key=True)
    SKU             = Column(Integer)
    QtyOrder        = Column(Integer)
    QtyReceived     = Column(Integer)
    PODate          = Column(DateTime)
    LineDescription = Column(String)
    Cost            = Column(Integer)
    Price           = Column(Integer)
    PriceWTax       = Column(Integer)
    UOMCode         = Column(String)
    Season          = Column(String, nullable=True)