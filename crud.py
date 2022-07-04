from sqlalchemy.orm import Session

from import models, schemas


def get_trade_by_id(db: Session, trade_id: str):
    return db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()

def get_trade(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trade).offset(skip).limit(limit).all()

def create_trade(db: Session, trade: schemas.Trade):
    db_trade = models.Trade(
        asset_class=trade.asset_class,
        counterparty=trade.counterparty,
        instrument_id=trade.instrument_id,
        instrument_name=trade.instrument_name,
        trade_date_time=trade.trade_date_time,
        trade_id=trade.trade_id,
        trader=trade.trader
    )
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade

def get_trade(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trade).offset(skip).limit(limit).all()

def create_trade_details(db: Session, trade_details: schemas.TradeDetails,trade_id: str):
    
    db_trade_details = models.TradeDetails(
        owner_id=trade_id,
        buySellIndicator=trade_details.buySellIndicator,
        price=trade_details.price,
        quantity=trade_details.quantity,
    )
    db.add(db_trade_details)
    db.commit()
    db.refresh(db_trade_details)
    return db_trade_details