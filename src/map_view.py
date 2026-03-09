"""
map_view.py - יצירת מפה אינטראקטיבית
"""

import folium


def sort_by_time(arr):
    """

    Args:
        arr: רשימת מילונים שמקבלים מאקסטרקתור

    Returns: רשימה מסודרת לפי תאריכים וזמן

    """
    return sorted(arr, key=lambda x: x["datetime"] if x["datetime"] else "")


def create_map(images_data):
    """
    יוצר מפה אינטראקטיבית עם כל המיקומים.

    Args:
        images_data: רשימת מילונים מ-extract_all

    Returns:
        string של HTML (המפה)
    """

    gps_images = [img for img in images_data if img["has_gps"]]

    if not gps_images:
        return "<h2>No GPS data found</h2>"

    center_lat = sum(img["latitude"] for img in gps_images) / len(gps_images)
    center_lon = sum(img["longitude"] for img in gps_images) / len(gps_images)

    m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    for img in gps_images:
        folium.Marker(
            location=[img["latitude"], img["longitude"]],
            popup=f"name - {img['filename']}<br>date - {img['datetime']}<br>phone model - {img['camera_model']}",
        ).add_to(m)

    return m._repr_html_()


if __name__ == "__main__":
    # יצירצ מפה עם fake_data
    # אחר כך נצתרך לשנות למה שחוזר מextractor
    # ועבר מיון דרך sort by time
    fake_data = [
        {"filename": "test1.jpg", "latitude": 32.0853, "longitude": 34.7818,
         "has_gps": True, "camera_make": "Samsung", "camera_model": "Galaxy S23",
         "datetime": "2025-01-12 08:30:00"},
        {"filename": "test2.jpg", "latitude": 31.7683, "longitude": 35.2137,
         "has_gps": True, "camera_make": "Apple", "camera_model": "iPhone 15 Pro",
         "datetime": "2025-01-13 09:00:00"},
    ]
    html = create_map(fake_data)
    with open("test_map.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Map saved to test_map.html")
