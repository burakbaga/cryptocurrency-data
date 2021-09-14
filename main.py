from fastapi import FastAPI,BackgroundTasks,Depends,Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
import models
from models import Crypto
from database import SessionLocal,engine
import yfinance as yf
import warnings

warnings.filterwarnings("ignore")
app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


class CryptoRequest(BaseModel):
    symbol : str

def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def home(request:Request,db:Session=Depends(get_db)):

    crypto = db.query(Crypto)
    print(crypto)

    return templates.TemplateResponse("home.html",{
        "request":request,
        "cryptoes":crypto,
    })

def fetch_all_data(id:int):
    db = SessionLocal()
    crypto = db.query(Crypto).filter(Crypto.id==id).first()

    yahoo = yf.download(tickers = f"{crypto.symbol}-USD",period="1d",interval="1d")
    crypto.open = yahoo["Open"].values[0]
    crypto.high = yahoo["High"].values[0]
    crypto.low = yahoo["Low"].values[0]
    crypto.close = yahoo["Close"].values[0]
    crypto.volume= int(yahoo["Volume"].values[0])

    db.add(crypto)
    db.commit()

@app.post("/crypto")
async def create_crypto_curr(crypto_request:CryptoRequest,background_tasks:BackgroundTasks,db : Session = Depends(get_db)):
    
    crypto = Crypto()
    crypto.symbol = crypto_request.symbol

    db.add(crypto)
    db.commit()

    print(crypto_request.symbol)

    background_tasks.add_task(fetch_all_data(crypto.id))

    return {
        "message":"cryptocurrency created"
    }