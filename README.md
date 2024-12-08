# OCR API ภาษาไทย พร้อมใช้งานใน Docker | Thai OCR API with Docker Support

API นี้ออกแบบมาเพื่อดึงข้อมูลจากรูปภาพด้วยเทคโนโลยี OCR (Optical Character Recognition) รองรับการใช้งานกับ Docker และสามารถใช้งานได้ทั้งภาษาไทยและภาษาอังกฤษ โดยมี Endpoint ที่ใช้งานได้ดังนี้:

This API is designed for extracting text from images using OCR (Optical Character Recognition) technology. It supports Docker and can process both Thai and English. The following endpoints are available:

---

## การติดตั้งและการใช้งาน | Installation and Usage

### 1. Clone Repository
```bash
git clone <repository-url>
cd <repository-folder>
2. ตั้งค่า Docker | Set Up Docker
ตรวจสอบให้แน่ใจว่าไฟล์ Dockerfile และ docker-compose.yml พร้อมใช้งานแล้ว
Ensure that Dockerfile and docker-compose.yml are properly configured.

3. สร้างและรัน Docker Container | Build and Run Docker Container
bash
คัดลอกโค้ด
docker-compose up --build
4. การใช้งาน API | Using the API
เมื่อ Container ทำงานสำเร็จ API จะพร้อมใช้งานที่ http://localhost:8000
Once the container is running, the API will be accessible at http://localhost:8000.

Endpoints
1. OCR ข้อมูลทั้งหมด | OCR All Data
URL: http://localhost:8000/ocr/rawdata/
Method: POST
Input:
รูปภาพ (Multipart Form Data) | Image (Multipart Form Data)
Output:
json
คัดลอกโค้ด
{
  "text": [
    "string"
  ]
}
2. OCR บัตรประชาชนไทย (รูปภาพ) | OCR Thai ID Card (Image)
URL: http://localhost:8000/ocr/thaiidcard/
Method: POST
Input:
รูปภาพ (Multipart Form Data) | Image (Multipart Form Data)
Output:
json
คัดลอกโค้ด
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
3. OCR บัตรประชาชนไทย (Base64) | OCR Thai ID Card (Base64)
URL: http://localhost:8000/ocr/thaiidcard/base64/
Method: POST
Input:
Base64 ของรูปภาพ | Base64 encoded image
Output:
json
คัดลอกโค้ด
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
ตัวอย่างคำขอ | Sample Requests
OCR ข้อมูลทั้งหมด | OCR All Data
bash
คัดลอกโค้ด
curl -X POST http://localhost:8000/ocr/rawdata/ \
-F "file=@path_to_image.jpg"
OCR บัตรประชาชนไทย (รูปภาพ) | OCR Thai ID Card (Image)
bash
คัดลอกโค้ด
curl -X POST http://localhost:8000/ocr/thaiidcard/ \
-F "file=@path_to_image.jpg"
OCR บัตรประชาชนไทย (Base64) | OCR Thai ID Card (Base64)
bash
คัดลอกโค้ด
curl -X POST http://localhost:8000/ocr/thaiidcard/base64/ \
-H "Content-Type: application/json" \
-d '{"image": "Base64_encoded_string_here"}'
การทดสอบ | Testing
สามารถใช้เครื่องมือเช่น Postman หรือ curl เพื่อส่งคำขอและตรวจสอบการทำงาน
Use tools like Postman or curl to send requests and validate functionality.

การพัฒนาเพิ่มเติม | Further Development
เพิ่ม Library หรือ Module | Add Libraries or Modules
อัปเดตไฟล์ requirements.txt และรันคำสั่ง: Update requirements.txt and run:

bash
คัดลอกโค้ด
docker-compose build
การ Debug | Debugging
ดู Log การทำงานของ Container ด้วยคำสั่ง: View container logs with:

bash
คัดลอกโค้ด
docker logs <container-id>
