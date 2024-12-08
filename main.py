from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import List, Optional
# import easyocr
import io
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import pytesseract
from models import OCRResponse,OCRResponsestr
import utils
import base64

app = FastAPI()

# Create an EasyOCR Reader instance
# reader = easyocr.Reader(['th', 'en'])  # 'th' for Thai, 'en' for English

# @app.post("/ocr/easyocr/", response_model=OCRResponsestr)
# async def perform_ocr_easyocr(file: UploadFile = File(...)):
#     try:
#         # Read the uploaded file
#         image = Image.open(io.BytesIO(await file.read()))
        
#         # Convert PIL Image to numpy array
#         image_np = np.array(image)

#         # Perform OCR using EasyOCR
#         results = reader.readtext(image_np)
        
#         # Extract the text from the results
#         extracted_text = [result[1] for result in results]
        
#         return OCRResponsestr(text=extracted_text)
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
class Base64ImageRequest(BaseModel):
    base64_str: str
    
@app.post("/ocr/rawdata/", response_model=OCRResponsestr)
async def perform_ocr_pytesseract(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        image = Image.open(io.BytesIO(await file.read()))
        im_gray = image.convert("L")
        im_gray.info['dpi'] = (300, 300)
        im_gray = im_gray.filter(ImageFilter.GaussianBlur(1))

        enhancer = ImageEnhance.Contrast(im_gray)
        enhanced_image = enhancer.enhance(2)
        
        # Perform OCR using Pytesseract
        text = pytesseract.image_to_string(enhanced_image, lang='tha+eng')
        
        # Split text into lines
        extracted_text = text.split('\n')

        return OCRResponsestr(text=extracted_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/ocr/thaiidcard/", response_model=OCRResponse)
async def perform_ocr_thaiidcard(file: UploadFile = File(...)):
    try:
        # Read the uploaded file
        image = Image.open(io.BytesIO(await file.read()))
        im_gray = image.convert("L")
        width, height = im_gray.size
        im_gray.info['dpi'] = (300, 300)
        im_gray = im_gray.filter(ImageFilter.GaussianBlur(1))

        enhancer = ImageEnhance.Contrast(im_gray)
        enhanced_image = enhancer.enhance(2)
        
        # Perform OCR using Pytesseract
        text = pytesseract.image_to_string(enhanced_image, lang='tha+eng')
        
        # Split text into lines
        extracted_text = [
            utils.clean_text(line)
            for line in text.split('\n')
            if line.strip()
        ]

        # datatext=[
        #     "Thai National ID Card",
        #     "เลขประจําตัวประชาชน   1 8099 00337 14 1",
        #     "Identification Number",
        #     "= ชื่อตัวและชื่อสกุล นาย ธงชัย บํารุงศรี",
        #     "๋          Name Mr. Tonge hai",
        #     "Lastname Bamrungsee",
        #     "เกิดวันที่ 2 W.8. 2533",
        #     "Date of Birth 2 Nov. 1990",
        #     "ที่อยู่ 51/2 หมู่ที่ 3 ต.ทุ่งสัง อ.ทุ่งใหญ่",
        #     "จุนครศรีธรรมราช",
        #     "1 WW. 2575",
        #     "วันบัตรหมดอายุ",
        #     "นายอรร  งูตํา          1 Nov. 2032",
        #     "เจ้าพนักง่านออกบัตร ก]๓!๐ of Expiry   10320411061012"
        #     ]
        extracted_data = utils.extract_information_from_text(extracted_text)
        
        # Check if required fields are empty
        if not (extracted_data.cardNumber and extracted_data.prename and extracted_data.firstname and extracted_data.lastname and extracted_data.birthDate):
            extracted_data.status = "failed"
            extracted_data.message = "Retry"
        
        return extracted_data
    
    except Exception as e:
        return OCRResponse(status="failed", message=f"An error occurred: {str(e)}")

@app.post("/ocr/thaiidcard/base64/", response_model=OCRResponse)
async def perform_ocr_thaiidcard_base64(request: Base64ImageRequest):
    try:
        # Decode the base64 string
        image_data = base64.b64decode(request.base64_str)
        image = Image.open(io.BytesIO(image_data))
        im_gray = image.convert("L")
        width, height = im_gray.size
        im_gray.info['dpi'] = (300, 300)
        im_gray = im_gray.filter(ImageFilter.GaussianBlur(1))

        enhancer = ImageEnhance.Contrast(im_gray)
        enhanced_image = enhancer.enhance(2)
        
        # Perform OCR using Pytesseract
        text = pytesseract.image_to_string(enhanced_image, lang='tha+eng')
        
        # Split text into lines
        extracted_text = [
            utils.clean_text(line)
            for line in text.split('\n')
            if line.strip()
        ]

        extracted_data = utils.extract_information_from_text(extracted_text)
        
        # Check if required fields are empty
        if not (extracted_data.cardNumber and extracted_data.prename and extracted_data.firstname and extracted_data.lastname and extracted_data.birthDate):
            extracted_data.status = "failed"
            extracted_data.message = "Retry"
        
        return extracted_data
    
    except Exception as e:
        return OCRResponse(status="failed", message=f"An error occurred: {str(e)}")
    
