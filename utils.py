import re
from models import OCRResponse
from typing import List, Optional

def clean_text(text: str) -> str:
    return text.replace('fies', 'ที่อยู่').replace('บัตรประจําตัวประชาชน', '').replace('จ.ุ', 'จ.').replace('จ. ', 'จ.').replace('จ ', 'จ.').replace('ต ', 'ต.').replace('ต. ', 'ต.').replace('อ ', 'อ.').replace('อ. ', 'อ.').replace('"', '').replace(',', '').replace('(', '').replace(')', '').replace('-', '').strip()

def is_thai_national_id(id: str) -> bool:
    if not (id.isdigit() and len(id) == 13):
        return False
    
    sum_ = 0
    for i in range(12):
        sum_ += int(id[i]) * (13 - i)
    
    check_sum = (11 - (sum_ % 11)) % 10
    return check_sum == int(id[12])

def remove_prefix(text, keyword):
    # ค้นหาตำแหน่งของ keyword ในสตริง
    index = text.find(keyword)
    if index != -1:
        # ตัดข้อความที่อยู่ข้างหน้าออก
        return text[index:].strip()
    return text
def format_address(address_name: str, checkstring: str) -> str:
    # เช็คว่าตัวอักษรตัวแรกเป็น checkstring หรือไม่
    if address_name.startswith(checkstring):
        # ตัด checkstring ออกและแทนที่ตัวอักษรตัวถัดไปเป็น "." เสมอ
        # ใช้ address_name[len(checkstring):] เพื่อรับส่วนที่เหลือหลัง checkstring
        remainder = address_name[len(checkstring):]
        
        # ลบเครื่องหมายจุลภาคและเว้นวรรคที่ไม่จำเป็น
        remainder = remainder.lstrip(',').strip()
        
        # รวม checkstring กับ "." และส่วนที่เหลือ
        return (checkstring + '.' + remainder).replace('..','.')
    
    return address_name.replace('..','.')


def extract_information_from_text(extracted_text: List[str]) -> OCRResponse:
    datas = OCRResponse()
    
    address_lines = []
    row:int=0
    rnext:int=0
    datas.rawocr = extracted_text

    for line in extracted_text:
        line = clean_text(line)
        
        cleaned_line = ''.join(line.split())
        keywords = ['เลข', 'ประ','จํา', 'ตัว', 'ประ','ชา','ชน']
        if any(keyword in cleaned_line for keyword in keywords):
            cleaned_line=remove_prefix(cleaned_line, "ชาชน")
            # card_number = cleaned_line.replace('ชาชน', '')
            card_number = re.findall(r'\d+', cleaned_line)
            card_number = ''.join(card_number)
            
            if is_thai_national_id(card_number):
                datas.cardNumber = card_number

        if 'สกุล' in line:
            line=remove_prefix(line, "สกุล")
            items = line.split()
            if len(items) >= 4:
                datas.prename = items[1]
                datas.firstname = items[2]
                datas.lastname = items[3]

        if row + 1 < len(extracted_text) :
            next_line = clean_text(extracted_text[row + 1])
            if 'name' in next_line and datas.firstname==None:
                # Set the current line as valid if the next line contains 'name'
                line2=remove_prefix(extracted_text[row - 1], "สกุล")
                items = line2.split()
                if len(items) >= 4:
                    datas.prename = items[1]
                    datas.firstname = items[2]
                    datas.lastname = items[3]

        if 'Date of Birth' in line:
            items = line.split()
            if len(items) >= 6:
                datas.birthDate = f"{items[3]} {items[4]} {items[5]}"
        
        if 'ที่อยู่' in line:
            line=remove_prefix(line, "ที่อยู่")
            address_lines.append(line.replace('ที่อยู่', '').strip())
            rnext = row+1
        
        if row == rnext and row != 0:
            address_lines.append(line.strip())    

        row += 1
    
    if address_lines:
        full_address = ' '.join(address_lines)
        address_parts = re.split(r'\s+', full_address)
        
        datas.address = full_address
        if len(address_parts) > 0:
            datas.addressno = address_parts[0]
        if len(address_parts) > 2:
            datas.moo = address_parts[2].strip()
        if len(address_parts) > 3:
            datas.subdistrict =format_address( address_parts[3].strip(),'ต')
        if len(address_parts) > 4:
            datas.district = format_address(address_parts[4].strip(),'อ')
        if len(address_parts) > 5:
            # datas.province = address_parts[5].strip()
            datas.province = format_address(address_parts[5].strip(),'จ')
    
    if datas.prename:
        datas.gender = 'M'
        if datas.prename in ['น.ส.', 'นางสาว', 'นาง', 'เด็กหญิง']:
            datas.gender = 'F'
    
    datas.status = "success"
    datas.message = "success"
    
    return datas

