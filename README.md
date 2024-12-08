# OCR API ภาษาไทย (รองรับ Docker)  
**Thai OCR API (Docker-Ready)**  

โปรเจคนี้เป็น API สำหรับ OCR ข้อความภาษาไทย รวมถึงการดึงข้อมูลจากบัตรประชาชนไทย  

This project is an API for performing OCR (Optical Character Recognition) on Thai text, including extracting data from Thai national ID cards.  

---

## คุณสมบัติ (Features)  
- **OCR ข้อความทั่วไป (General OCR):** อัพโหลดรูปภาพเพื่ออ่านข้อความภาษาไทย (Upload an image to extract Thai text).  
- **OCR บัตรประชาชนไทย (Thai National ID OCR):** รองรับ input ทั้งรูปภาพและ Base64 (Supports image and Base64 input).  
- รองรับการใช้งานผ่าน Docker (Docker-ready).  

---

## วิธีติดตั้ง (Installation)  

### ใช้งานด้วย Docker (Using Docker)  
1. สร้าง Docker Image (Build the Docker image):  
    ```bash
    docker build -t ocr-api .
    ```  
2. รัน Docker Container (Run the Docker container):  
    ```bash
    docker run -d -p 8000:8000 ocr-api
    ```  

### รันในเครื่อง (Run Locally)  
1. ติดตั้ง Dependency (Install dependencies):  
    ```bash
    pip install -r requirements.txt
    ```  
2. รันเซิร์ฟเวอร์ (Run the server):  
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```  

---

## วิธีการใช้งาน (Usage)  

### Endpoints  

#### 1. OCR ข้อความทั่วไป (General OCR)  
- **URL:** `/ocr/rawdata/`  
- **Method:** `POST`  
- **Input:** อัพโหลดไฟล์รูปภาพ (Upload an image).  
- **Output:**  
    ```json
    {
        "text": [
            "string"
        ]
    }
    ```  

#### 2. OCR บัตรประชาชนไทย (Thai National ID OCR - Image Input)  
- **URL:** `/ocr/thaiidcard/`  
- **Method:** `POST`  
- **Input:** อัพโหลดไฟล์รูปภาพ (Upload an image).  
- **Output:**  
    ```json
    {
        "cardNumber": "string",
        "prename": "string",
        "firstname": "string",
        "lastname": "string",
        "birthDate": "string",
        "address": "string",
        "addressno": "string",
        "moo": "string",
        "subdistrict": "string",
        "district": "string",
        "province": "string",
        "gender": "string",
        "status": "failed",
        "message": "error",
        "rawocr": [
            "string"
        ]
    }
    ```  

#### 3. OCR บัตรประชาชนไทย (Thai National ID OCR - Base64 Input)  
- **URL:** `/ocr/thaiidcard/base64/`  
- **Method:** `POST`  
- **Input:** JSON object with a Base64-encoded image:  
    ```json
    {
        "base64_string": "BASE64_ENCODED_IMAGE"
    }
    ```  
- **Output:** Same as above.  

---

## ตัวอย่างการใช้งาน (Examples)  

### ด้วย cURL (Using cURL)  

#### 1. OCR ข้อความทั่วไป (General OCR)  
```bash
curl -X POST "http://localhost:8000/ocr/rawdata/" \
-F "file=@path_to_image.jpg"
