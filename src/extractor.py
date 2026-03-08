from PIL import Image
from PIL.ExifTags import TAGS
from pathlib import Path
import os

"""
extractor.py - שליפת EXIF מתמונות
צוות 1, זוג A

ראו docs/api_contract.md לפורמט המדויק של הפלט.

"""


def dms_to_decimal(dms, ref):
    if not dms or not ref:
        return None

    degrees = dms[0]
    minutes = dms[1]
    seconds = dms[2]
    # to convert from degrees minutes and seconds to decimal float
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

    if ref in ['S', 'W']:
        decimal = -decimal

    return float(decimal)


def has_gps(data: dict):
    return 'GPSInfo' in data and len(data['GPSInfo']) > 0


def latitude(data: dict):
    if has_gps(data):
        gps_info = data['GPSInfo']
        return dms_to_decimal(gps_info.get(2), gps_info.get(1))
    return None


def longitude(data: dict):
    if has_gps(data):
        gps_info = data['GPSInfo']
        return dms_to_decimal(gps_info.get(4), gps_info.get(3))
    return None


def datatime(data: dict):
    date = data.get("DateTimeOriginal")

    if date:
        formatted_date = date.replace(':', '-', 2)
        return formatted_date


def camera_make(data: dict):
    make = data.get("Make")
    return make


def camera_model(data: dict):
    model = data.get("Model")
    return model


def extract_metadata(image_path):
    """
    שולף EXIF מתמונה בודדת.

    Args:
        image_path: נתיב לקובץ תמונה

    Returns:
        dict עם: filename, datetime, latitude, longitude,
              camera_make, camera_model, has_gps
    """
    path = Path(image_path)

    # תיקון: טיפול בתמונה בלי EXIF - בלי זה, exif.items() נופל עם AttributeError
    try:
        img = Image.open(image_path)
        exif = img._getexif()
    except Exception:
        exif = None

    if exif is None:
        return {
            "filename": path.name,
            "datetime": None,
            "latitude": None,
            "longitude": None,
            "camera_make": None,
            "camera_model": None,
            "has_gps": False
        }

    data = {}
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value

    # תיקון: הוסר print(data) שהיה כאן - הדפיס את כל ה-EXIF הגולמי על כל תמונה

    exif_dict = {
        "filename": path.name,
        "datetime": datatime(data),
        "latitude": latitude(data),
        "longitude": longitude(data),
        "camera_make": camera_make(data),
        "camera_model": camera_model(data),
        "has_gps": has_gps(data)
    }
    return exif_dict


def extract_all(folder_path):
    """
    שולף EXIF מכל התמונות בתיקייה.

    Args:
        folder_path: נתיב לתיקייה

    Returns:
        list של dicts (כמו extract_metadata)
    """
    all_data_list = []
    files = os.listdir(folder_path)

    for filename in files:
        if filename.lower().endswith(('.jpg', '.jpeg')):
            full_path = os.path.join(folder_path, filename)
            all_data_list.append(extract_metadata(full_path))

    return all_data_list

# to test change to your local path
# print(extract_all("/Users/danielkhabirkhanov/Study/KodKode/image_intel/image_intel_the_winning_team/images/ready"))
