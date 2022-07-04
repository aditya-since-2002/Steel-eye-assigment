# STEELEYSE API ASSESSMENT


[![N|Solid](https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png)](https://fastapi.tiangolo.com/)

- Hey there
-  ✨let's begin✨

## Installation using cmd

> pip install fastapi

> pip install "uvicorn[standard]"

## What is SQLAlchemy?

SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.

It provides a full suite of well known enterprise-level persistence patterns, designed for efficient and high-performing database access, adapted into a simple and Pythonic domain language.

Read more about[ SQLAlchemy](https://www.sqlalchemy.org/) on their official site.



## File structure
For these examples, let's say you have a directory named my_super_project that contains a sub-directory called sql_app with a structure like this:
.
└── sql_app
    ├── _init_.py
    ├── crud.py
    ├── database.py
    ├── main.py
    ├── models.py
    └── schemas.py
    
The file _init_.py is just an empty file, but it tells Python that sql_app with all its modules (Python files) is a package.

Now let's see what each file/module does.

## Create the SQLAlchemy parts¶
Let's refer to the file sql_app/database.py.

## Import the SQLAlchemy parts¶

The import of create_engine, declarative_base and sessionmaker were done.
The create_engine() function produces an Engine object based on a URL.
>from sqlalchemy import create_engine

The declarative_base() base class contains a MetaData object where newly defined Table objects are collected.
>from sqlalchemy.ext.declarative import declarative_base

Session class is defined using sessionmaker() – a configurable session factory method which is bound to the engine object created earlier.
>from sqlalchemy.orm import sessionmaker

>SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


## Create a database URL for SQLAlchemy

This is the entire working of database.py 

---
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

>The import of the files has been made

SQLALCHEMY_DATABASE_URL = 'sqlite:///./steeleye.db'

>The database URI that should be used for the connection.

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

---


## Create the database models¶

Let's now see the file sql_app/models.py.

Create SQLAlchemy models from the Base class¶
We will use this Base class we created before to create the SQLAlchemy models.

---
sh
from sqlalchemy import Column, Integer, ForeignKey ,String, Float, Boolean,DateTime 

>As known the Column, Integer, ForeignKey ,String, Float, Boolean,DateTime  are the part of data types which are used in SQL as well

from sqlalchemy.orm import relationship

> It provides a relationship between two mapped classes.


from database import Base

>database design philosophy that prizes Availability over Consistency of operations. 

>Two differents are created below one is tradedetails and the other one is trade with various properties inside

class TradeDetails(Base):
    __tablename__ = "trade_details"

    id = Column(String, primary_key=True, index=True)
    buySellIndicator = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    trades = relationship("Trade", back_populates='trade_details')


class Trade(Base):
    __tablename__ = "trade"

    asset_class = Column(String)
    counterparty = Column(String)
    instrument_id = Column(Integer)
    instrument_name = Column(String)
    trade_date_time = Column(DateTime)
    trade_details_id = Column(String, ForeignKey("trade_details.id"))
    trade_details = relationship("TradeDetails", back_populates='trades')
    trade_id = Column(String, primary_key=True, index=True)
    trader = Column(String)

---


## Create the Pydantic models¶
Now let's check the file sql_app/schemas.py.


### Create initial Pydantic models / schemas¶

>Create an trade and tradedetails Pydantic models (or let's say "schemas") to have common attributes while creating or reading data and create an trade and tradedetails that inherit from them (so they will have the same attributes), plus any additional data (attributes) needed for creation.

>So, the user will also have a password when creating it.

**But for security, the password won't be in other Pydantic models, for example, it won't be sent from the API when reading a user**

---

sh
import datetime as dt

from typing import Optional , List
from pydantic import BaseModel, Field

class TradeDetails(BaseModel):
    buySellIndicator: str = Field(description="A value of BUY for buys, SELL for sells.")

    price: float = Field(description="The price of the Trade.")

    quantity: int = Field(description="The amount of units traded.")


class Trade(BaseModel):
    asset_class: Optional[str] = Field(alias="assetClass", default=None, description="The asset class of the instrument traded. E.g. Bond, Equity, FX...etc")

    counterparty: Optional[str] = Field(default=None, description="The counterparty the trade was executed with. May not always be available")

    instrument_id: str = Field(alias="instrumentId", description="The ISIN/ID of the instrument traded. E.g. TSLA, AAPL, AMZN...etc")

    instrument_name: str = Field(alias="instrumentName", description="The name of the instrument traded.")

    trade_date_time: dt.datetime = Field(alias="tradeDateTime", description="The date-time the Trade was executed")

    trade_details: List[TradeDetails] = Field(alias="tradeDetails", description="The details of the trade, i.e. price, quantity")

    trade_id: str = Field(alias="tradeId", default=None, description="The unique ID of the trade")

    trader: str = Field(description="The name of the Trader")

---

## CRUD utils¶

Now let's see the file sql_app/crud.py.

In this file we will have reusable functions to interact with the data in the database.

>CRUD comes from: Create, Read, Update, and Delete.

...although in this example we are only creating and reading.

### Read data¶
Import Session from sqlalchemy.orm, this will allow you to declare the type of the db parameters and have better type checks and completion in your functions.


>Import models (the SQLAlchemy models) and schemas (the Pydantic models / schemas).


#### Create utility functions to:

- Read a single user by ID and by email.
- Read multiple users.
- Read multiple items.

#### Create data¶

Now create utility functions to create data.

The steps are:

- Create a SQLAlchemy model instance with your data.
- add that instance object to your database session.
- commit the changes to the database (so that they are saved).
- refresh your instance (so that it contains any new data from the database, like the generated ID).

---

sh
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

---

## Main FastAPI app¶
And now in the file sql_app/main.py let's integrate and use all the other parts we created before.

**Create the database tables¶**

In a very simplistic way create the database tables:

---

sh
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException,Request,Response
from sqlalchemy.orm import Session
import schemas, models # noqa: E402

from database import SessionLocal,engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.get("/trades")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.Trade).limit(limit).all()


@app.post("/trade")
async def create_trade(trades: schemas.Trade, db: Session = Depends(get_db)):
    db_trade=db.query(models.Trade).filter(models.Trade.trade_id == trades.trade_id).first()
    if db_trade:
        raise HTTPException(status_code=400, detail="Trade already exists")
    new_trade = models.Trade(trade_id=trades.trade_id, trader=trades.trader, asset_class=trades.asset_class,
                             counterparty=trades.counterparty, trade_date_time=trades.trade_date_time,
                             instrument_id=trades.instrument_id, instrument_name=trades.instrument_name)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

@app.post("/trade_details/{id}")
async def create_trade_details(trade_details: schemas.TradeDetails, id: str, db: Session = Depends(get_db)):
    new_trade_details = models.TradeDetails(id=id, buySellIndicator=trade_details.buySellIndicator,
                                            price=trade_details.price, quantity=trade_details.quantity)
    db.add(new_trade_details)
    db.commit()
    db.refresh(new_trade_details)
    return new_trade_details

@app.get("/trade/{trade_id}")
async def get_trade_by_id(trade_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    
@app.get("/trade/{counterparty}/details")
async def get_trade_by_counterparty(counterparty: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.counterparty == counterparty).all()

@app.get("/trade/{trader}/details")
async def get_trade_by_trader(trader: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trader == trader).all()


@app.get("/trade/{instrument_id}/details")
async def get_trade_by_instrument_id(instrument_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.instrument_id == instrument_id).all()

@app.get("/trade/{instrument_name}/details")
async def get_trade_by_instrument_name(instrument_name: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.instrument_name == instrument_name).all()

---

## Create a dependency¶
Now use the SessionLocal class we created in the sql_app/database.py file to create a dependency.

We need to have an independent database session/connection (SessionLocal) per request, use the same session through all the request and then close it after the request is finished.

And then a new session will be created for the next request.

For that, we will create a new dependency with yield, as explained before in the section about Dependencies with yield.

Our dependency will create a new SQLAlchemy SessionLocal that will be used in a single request, and then close it once the request is finished.

---

sh
from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException,Request,Response
from sqlalchemy.orm import Session
import schemas, models # noqa: E402

from database import SessionLocal,engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

---

# Dependency

---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/trades")
async def get_trades(db: Session = Depends(get_db), limit: Optional[int] = None):
    return db.query(models.Trade).limit(limit).all()


@app.post("/trade")
async def create_trade(trades: schemas.Trade, db: Session = Depends(get_db)):
    db_trade=db.query(models.Trade).filter(models.Trade.trade_id == trades.trade_id).first()
    if db_trade:
        raise HTTPException(status_code=400, detail="Trade already exists")
    new_trade = models.Trade(trade_id=trades.trade_id, trader=trades.trader, asset_class=trades.asset_class,
                             counterparty=trades.counterparty, trade_date_time=trades.trade_date_time,
                             instrument_id=trades.instrument_id, instrument_name=trades.instrument_name)
    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)
    return new_trade

@app.post("/trade_details/{id}")
async def create_trade_details(trade_details: schemas.TradeDetails, id: str, db: Session = Depends(get_db)):
    new_trade_details = models.TradeDetails(id=id, buySellIndicator=trade_details.buySellIndicator,
                                            price=trade_details.price, quantity=trade_details.quantity)
    db.add(new_trade_details)
    db.commit()
    db.refresh(new_trade_details)
    return new_trade_details

@app.get("/trade/{trade_id}")
async def get_trade_by_id(trade_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trade_id == trade_id).first()
    
@app.get("/trade/{counterparty}/details")
async def get_trade_by_counterparty(counterparty: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.counterparty == counterparty).all()

@app.get("/trade/{trader}/details")
async def get_trade_by_trader(trader: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.trader == trader).all()


@app.get("/trade/{instrument_id}/details")
async def get_trade_by_instrument_id(instrument_id: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.instrument_id == instrument_id).all()

@app.get("/trade/{instrument_name}/details")
async def get_trade_by_instrument_name(instrument_name: str, db: Session = Depends(get_db)):
    return db.query(models.Trade).filter(models.Trade.instrument_name == instrument_name).all()

---

## Check it¶
You can copy this code and use it as is.

Info

In fact, the code shown here is part of the tests. As most of the code in these docs.

Then you can run it with Uvicorn:

sh
uvicorn sql_app.main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)


And then, you can open your browser at http://127.0.0.1:8000/docs.

And you will be able to interact with your FastAPI application, reading data from a real database:

## Interact with the database directly¶
If you want to explore the SQLite database (file) directly, independently of FastAPI, to debug its contents, add tables, columns, records, modify data, etc. you can use DB Browser for SQLite.

It will look like this: