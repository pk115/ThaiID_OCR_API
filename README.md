Thai ID Card OCR API
This is a Python API for Optical Character Recognition (OCR) specifically designed for the Thai language. The API supports general OCR as well as OCR for Thai National ID cards. Inputs can be provided as images or Base64-encoded strings.

Features
General OCR: Extract text from any image containing Thai text.
OCR Thai National ID Card (Image Input): Extract structured information from Thai National ID cards by providing an image file.
OCR Thai National ID Card (Base64 Input): Extract structured information from Thai National ID cards using a Base64-encoded image string.

# OCR API ภาษาไทย (รองรับ Docker)

โปรเจคนี้เป็น API สำหรับ OCR ข้อความภาษาไทย รวมถึงการดึงข้อมูลจากบัตรประชาชนไทย

## คุณสมบัติ
- **OCR ข้อความทั่วไป:** อัพโหลดรูปภาพเพื่ออ่านข้อความภาษาไทย
- **OCR บัตรประชาชนไทย:** รองรับ input ทั้งรูปภาพและ Base64
- รองรับการใช้งานผ่าน Docker

## วิธีติดตั้ง

### ใช้งานด้วย Docker
1. สร้าง Docker Image
    ```bash
    docker build -t ocr-api .
    ```
2. รัน Docker Container
    ```bash
    docker run -d -p 8000:8000 ocr-api
    ```

### รันในเครื่อง
1. ติดตั้ง Dependency
    ```bash
    pip install -r requirements.txt
    ```
2. รันเซิร์ฟเวอร์
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## วิธีการใช้งาน

### Endpoint
1. **OCR ข้อความทั่วไป**
    - URL: `/ocr/all/`
    - Method: `POST`
    - Payload: อัพโหลดไฟล์รูปภาพ
2. **OCR บัตรประชาชนไทย (Input เป็นรูปภาพ)**
    - URL: `/ocr/idcard/image/`
    - Method: `POST`
    - Payload: อัพโหลดไฟล์รูปภาพ
3. **OCR บัตรประชาชนไทย (Input เป็น Base64)**
    - URL: `/ocr/idcard/base64/`
    - Method: `POST`
    - Payload: JSON 
      ```json
      {
          "base64_string": "BASE64_ENCODED_IMAGE"
      }
      ```

### ตัวอย่างการใช้งาน
#### ด้วย cURL
```bash
curl -X POST "http://localhost:8000/ocr/all/" \
-F "image=@path_to_image.jpg"
