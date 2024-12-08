from typing import List, Optional
from pydantic import BaseModel

class OCRResponsestr(BaseModel):
    text: List[str]

class OCRResponse(BaseModel):
    cardNumber: Optional[str] = None
    prename: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    birthDate: Optional[str] = None
    address: Optional[str] = None
    addressno: Optional[str] = None
    moo: Optional[str] = None
    subdistrict: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    gender: Optional[str] = None
    status: str = "failed"
    message: str = "error"
    rawocr: Optional[List[str]]=None

    