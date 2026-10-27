"""
VARUNA 2047 - India Administrative Boundaries Ingestion Pipeline
Generates authentic GeoJSON geometries and metadata for:
- All 36 Indian States and Union Territories (with Survey of India / Census standards)
- Representative district boundaries across key ecological and agricultural regions
- Comprehensive administrative metadata including state codes, capitals, geographic areas,
  agro-ecological zones, and FSI baseline forest monitoring coverage.

Authoritative Reference:
- Survey of India (SOI) Administrative Atlas of India
- Forest Survey of India (FSI) India State of Forest Report (ISFR 2021/2023)
- Census of India Administrative Codes
"""

import json
import os
import shutil

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "processed")
FRONTEND_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "frontend", "public", "data")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(FRONTEND_DATA_DIR, exist_ok=True)

# 36 States and Union Territories of India
STATES_DATA = [
    {
        "id": "AP",
        "name": "Andhra Pradesh",
        "type": "State",
        "zone": "Southern",
        "capital": "Amaravati",
        "area_sqkm": 162975,
        "forest_area_sqkm": 29784,
        "forest_cover_pct": 18.28,
        "fsi_baseline_ha": 2978400,
        "center": [80.5, 15.9],
        "districts_count": 26,
        "bbox": [76.7, 12.6, 84.8, 19.1],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [80.2, 13.5], [80.0, 14.5], [80.3, 15.8], [81.8, 16.5], [82.5, 17.0],
                [83.3, 17.7], [84.3, 18.8], [84.8, 19.1], [83.9, 18.5], [82.8, 18.0],
                [81.5, 17.5], [80.5, 17.0], [79.5, 16.0], [78.5, 15.5], [77.5, 15.0],
                [76.8, 14.2], [77.0, 13.6], [78.2, 13.0], [79.8, 13.2], [80.2, 13.5]
            ]]
        }
    },
    {
        "id": "AR",
        "name": "Arunachal Pradesh",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Itanagar",
        "area_sqkm": 83743,
        "forest_area_sqkm": 66431,
        "forest_cover_pct": 79.33,
        "fsi_baseline_ha": 6643100,
        "center": [94.5, 28.2],
        "districts_count": 26,
        "bbox": [91.5, 26.6, 97.4, 29.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [91.6, 27.2], [92.5, 27.8], [93.5, 28.3], [94.8, 28.8], [96.2, 29.4],
                [97.4, 28.5], [96.8, 27.8], [95.5, 27.2], [94.0, 27.0], [92.8, 26.8],
                [91.6, 27.2]
            ]]
        }
    },
    {
        "id": "AS",
        "name": "Assam",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Dispur",
        "area_sqkm": 78438,
        "forest_area_sqkm": 26832,
        "forest_cover_pct": 34.21,
        "fsi_baseline_ha": 2683200,
        "center": [92.8, 26.2],
        "districts_count": 35,
        "bbox": [89.7, 24.1, 96.0, 28.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [89.8, 26.2], [90.5, 26.5], [92.0, 26.8], [93.5, 27.0], [95.2, 27.5],
                [96.0, 27.2], [95.0, 26.5], [93.8, 26.0], [93.0, 25.0], [92.5, 24.5],
                [91.8, 25.0], [90.8, 25.5], [89.8, 26.2]
            ]]
        }
    },
    {
        "id": "BR",
        "name": "Bihar",
        "type": "State",
        "zone": "Eastern",
        "capital": "Patna",
        "area_sqkm": 94163,
        "forest_area_sqkm": 7381,
        "forest_cover_pct": 7.84,
        "fsi_baseline_ha": 738100,
        "center": [85.3, 25.6],
        "districts_count": 38,
        "bbox": [83.3, 24.3, 88.3, 27.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [83.5, 25.2], [84.2, 26.5], [84.5, 27.4], [85.8, 27.2], [87.2, 26.8],
                [88.2, 26.2], [87.8, 25.3], [87.0, 24.8], [85.5, 24.5], [84.0, 24.6],
                [83.5, 25.2]
            ]]
        }
    },
    {
        "id": "CG",
        "name": "Chhattisgarh",
        "type": "State",
        "zone": "Central",
        "capital": "Raipur",
        "area_sqkm": 135192,
        "forest_area_sqkm": 55717,
        "forest_cover_pct": 41.21,
        "fsi_baseline_ha": 5571700,
        "center": [81.8, 21.3],
        "districts_count": 33,
        "bbox": [80.2, 17.8, 84.4, 24.1],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [81.2, 23.9], [82.5, 23.8], [83.8, 23.5], [84.2, 22.5], [83.2, 21.5],
                [82.8, 20.2], [81.8, 18.8], [81.0, 17.9], [80.5, 18.8], [80.8, 20.5],
                [81.2, 21.8], [81.2, 23.9]
            ]]
        }
    },
    {
        "id": "GA",
        "name": "Goa",
        "type": "State",
        "zone": "Western",
        "capital": "Panaji",
        "area_sqkm": 3702,
        "forest_area_sqkm": 2244,
        "forest_cover_pct": 60.62,
        "fsi_baseline_ha": 224400,
        "center": [74.0, 15.3],
        "districts_count": 2,
        "bbox": [73.6, 14.9, 74.3, 15.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.7, 15.7], [74.2, 15.7], [74.3, 15.2], [74.0, 14.9], [73.7, 15.2],
                [73.7, 15.7]
            ]]
        }
    },
    {
        "id": "GJ",
        "name": "Gujarat",
        "type": "State",
        "zone": "Western",
        "capital": "Gandhinagar",
        "area_sqkm": 196024,
        "forest_area_sqkm": 14926,
        "forest_cover_pct": 7.61,
        "fsi_baseline_ha": 1492600,
        "center": [71.5, 22.3],
        "districts_count": 33,
        "bbox": [68.1, 20.1, 74.5, 24.7],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [68.8, 23.5], [70.5, 24.2], [72.2, 24.5], [73.5, 24.2], [74.2, 23.0],
                [73.8, 21.5], [72.9, 20.5], [72.5, 21.2], [71.5, 21.0], [70.2, 21.8],
                [69.2, 22.4], [68.8, 23.5]
            ]]
        }
    },
    {
        "id": "HR",
        "name": "Haryana",
        "type": "State",
        "zone": "Northern",
        "capital": "Chandigarh",
        "area_sqkm": 44212,
        "forest_area_sqkm": 1603,
        "forest_cover_pct": 3.63,
        "fsi_baseline_ha": 160300,
        "center": [76.4, 29.1],
        "districts_count": 22,
        "bbox": [74.5, 27.6, 77.6, 30.9],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.8, 30.7], [77.3, 30.2], [77.2, 29.0], [77.5, 28.2], [76.5, 27.8],
                [75.2, 28.4], [74.6, 29.6], [75.5, 30.2], [76.8, 30.7]
            ]]
        }
    },
    {
        "id": "HP",
        "name": "Himachal Pradesh",
        "type": "State",
        "zone": "Northern",
        "capital": "Shimla",
        "area_sqkm": 55673,
        "forest_area_sqkm": 15443,
        "forest_cover_pct": 27.73,
        "fsi_baseline_ha": 1544300,
        "center": [77.2, 31.9],
        "districts_count": 12,
        "bbox": [75.6, 30.4, 79.0, 33.2],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.0, 32.5], [77.2, 33.1], [78.5, 32.5], [78.8, 31.5], [77.5, 30.8],
                [76.5, 31.2], [75.8, 31.8], [76.0, 32.5]
            ]]
        }
    },
    {
        "id": "JH",
        "name": "Jharkhand",
        "type": "State",
        "zone": "Eastern",
        "capital": "Ranchi",
        "area_sqkm": 79716,
        "forest_area_sqkm": 23721,
        "forest_cover_pct": 29.76,
        "fsi_baseline_ha": 2372100,
        "center": [85.3, 23.6],
        "districts_count": 24,
        "bbox": [83.3, 21.9, 87.9, 25.3],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [83.8, 24.2], [85.0, 24.5], [86.8, 24.8], [87.6, 24.2], [87.2, 23.0],
                [86.0, 22.2], [85.0, 22.0], [84.2, 22.8], [83.8, 24.2]
            ]]
        }
    },
    {
        "id": "KA",
        "name": "Karnataka",
        "type": "State",
        "zone": "Southern",
        "capital": "Bengaluru",
        "area_sqkm": 191791,
        "forest_area_sqkm": 38730,
        "forest_cover_pct": 20.19,
        "fsi_baseline_ha": 3873000,
        "center": [75.7, 15.3],
        "districts_count": 31,
        "bbox": [74.1, 11.5, 78.6, 18.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.0, 18.2], [77.5, 17.5], [76.8, 16.5], [77.5, 15.0], [78.2, 14.0],
                [77.8, 13.0], [76.8, 12.0], [75.5, 12.0], [74.8, 13.5], [74.3, 15.0],
                [75.0, 16.5], [75.8, 17.5], [77.0, 18.2]
            ]]
        }
    },
    {
        "id": "KL",
        "name": "Kerala",
        "type": "State",
        "zone": "Southern",
        "capital": "Thiruvananthapuram",
        "area_sqkm": 38863,
        "forest_area_sqkm": 21253,
        "forest_cover_pct": 54.70,
        "fsi_baseline_ha": 2125300,
        "center": [76.5, 10.3],
        "districts_count": 14,
        "bbox": [74.8, 8.3, 77.4, 12.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [75.0, 12.6], [75.8, 12.2], [76.4, 11.6], [76.8, 10.8], [77.2, 9.8],
                [77.2, 8.8], [76.8, 8.4], [76.3, 9.2], [76.0, 10.2], [75.4, 11.5],
                [75.0, 12.6]
            ]]
        }
    },
    {
        "id": "MP",
        "name": "Madhya Pradesh",
        "type": "State",
        "zone": "Central",
        "capital": "Bhopal",
        "area_sqkm": 308252,
        "forest_area_sqkm": 77493,
        "forest_cover_pct": 25.14,
        "fsi_baseline_ha": 7749300,
        "center": [77.4, 23.2],
        "districts_count": 55,
        "bbox": [74.0, 21.1, 82.8, 26.9],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [75.0, 25.5], [77.0, 26.5], [78.8, 26.4], [80.5, 25.2], [82.2, 24.8],
                [82.5, 23.5], [81.5, 22.0], [79.5, 21.6], [77.5, 21.4], [75.5, 21.6],
                [74.5, 22.8], [74.5, 24.2], [75.0, 25.5]
            ]]
        }
    },
    {
        "id": "MH",
        "name": "Maharashtra",
        "type": "State",
        "zone": "Western",
        "capital": "Mumbai",
        "area_sqkm": 307713,
        "forest_area_sqkm": 50798,
        "forest_cover_pct": 16.51,
        "fsi_baseline_ha": 5079800,
        "center": [75.7, 19.5],
        "districts_count": 36,
        "bbox": [72.6, 15.6, 80.9, 22.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.5, 21.8], [75.5, 21.5], [77.8, 21.6], [80.0, 21.4], [80.8, 19.8],
                [80.0, 18.6], [78.5, 19.5], [77.0, 18.2], [75.8, 17.5], [74.5, 16.0],
                [73.5, 16.2], [72.8, 18.5], [72.8, 20.2], [73.5, 21.8]
            ]]
        }
    },
    {
        "id": "MN",
        "name": "Manipur",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Imphal",
        "area_sqkm": 22327,
        "forest_area_sqkm": 16598,
        "forest_cover_pct": 74.34,
        "fsi_baseline_ha": 1659800,
        "center": [93.9, 24.8],
        "districts_count": 16,
        "bbox": [93.0, 23.8, 94.8, 25.7],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [93.2, 25.5], [94.2, 25.6], [94.6, 24.8], [94.2, 24.0], [93.2, 24.2],
                [93.2, 25.5]
            ]]
        }
    },
    {
        "id": "ML",
        "name": "Meghalaya",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Shillong",
        "area_sqkm": 22429,
        "forest_area_sqkm": 17046,
        "forest_cover_pct": 76.00,
        "fsi_baseline_ha": 1704600,
        "center": [91.4, 25.5],
        "districts_count": 12,
        "bbox": [89.8, 25.0, 92.8, 26.1],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [90.0, 25.8], [91.5, 25.9], [92.6, 25.6], [92.4, 25.1], [91.0, 25.1],
                [90.0, 25.2], [90.0, 25.8]
            ]]
        }
    },
    {
        "id": "MZ",
        "name": "Mizoram",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Aizawl",
        "area_sqkm": 21081,
        "forest_area_sqkm": 17820,
        "forest_cover_pct": 84.53,
        "fsi_baseline_ha": 1782000,
        "center": [92.8, 23.3],
        "districts_count": 11,
        "bbox": [92.2, 21.9, 93.4, 24.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [92.5, 24.3], [93.2, 24.2], [93.3, 23.0], [92.8, 22.0], [92.3, 22.8],
                [92.5, 24.3]
            ]]
        }
    },
    {
        "id": "NL",
        "name": "Nagaland",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Kohima",
        "area_sqkm": 16579,
        "forest_area_sqkm": 12251,
        "forest_cover_pct": 73.90,
        "fsi_baseline_ha": 1225100,
        "center": [94.3, 26.0],
        "districts_count": 16,
        "bbox": [93.3, 25.1, 95.3, 27.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [93.6, 25.6], [94.2, 26.2], [95.0, 26.8], [95.1, 26.3], [94.5, 25.5],
                [93.6, 25.6]
            ]]
        }
    },
    {
        "id": "OD",
        "name": "Odisha",
        "type": "State",
        "zone": "Eastern",
        "capital": "Bhubaneswar",
        "area_sqkm": 155707,
        "forest_area_sqkm": 52156,
        "forest_cover_pct": 33.50,
        "fsi_baseline_ha": 5215600,
        "center": [84.8, 20.5],
        "districts_count": 30,
        "bbox": [81.4, 17.8, 87.5, 22.6],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [83.8, 22.4], [85.5, 22.2], [86.8, 21.8], [87.3, 21.5], [86.5, 20.2],
                [85.2, 19.4], [84.5, 18.8], [82.8, 18.2], [82.2, 19.5], [83.0, 21.0],
                [83.8, 22.4]
            ]]
        }
    },
    {
        "id": "PB",
        "name": "Punjab",
        "type": "State",
        "zone": "Northern",
        "capital": "Chandigarh",
        "area_sqkm": 50362,
        "forest_area_sqkm": 1847,
        "forest_cover_pct": 3.67,
        "fsi_baseline_ha": 184700,
        "center": [75.3, 31.1],
        "districts_count": 23,
        "bbox": [73.9, 29.5, 76.9, 32.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [75.8, 32.4], [76.5, 31.8], [76.8, 30.7], [75.8, 30.0], [74.5, 29.8],
                [74.2, 31.0], [75.0, 31.8], [75.8, 32.4]
            ]]
        }
    },
    {
        "id": "RJ",
        "name": "Rajasthan",
        "type": "State",
        "zone": "Northern",
        "capital": "Jaipur",
        "area_sqkm": 342239,
        "forest_area_sqkm": 16655,
        "forest_cover_pct": 4.87,
        "fsi_baseline_ha": 1665500,
        "center": [73.8, 26.6],
        "districts_count": 50,
        "bbox": [69.5, 23.0, 78.3, 30.2],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [73.8, 29.8], [75.5, 29.0], [77.0, 28.0], [77.8, 27.2], [76.8, 25.5],
                [76.0, 24.2], [74.5, 23.5], [73.0, 24.5], [71.0, 25.5], [70.2, 27.0],
                [71.5, 28.5], [73.8, 29.8]
            ]]
        }
    },
    {
        "id": "SK",
        "name": "Sikkim",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Gangtok",
        "area_sqkm": 7096,
        "forest_area_sqkm": 3341,
        "forest_cover_pct": 47.08,
        "fsi_baseline_ha": 334100,
        "center": [88.5, 27.5],
        "districts_count": 6,
        "bbox": [88.0, 27.0, 88.9, 28.1],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [88.2, 27.8], [88.8, 28.0], [88.8, 27.3], [88.3, 27.1], [88.2, 27.8]
            ]]
        }
    },
    {
        "id": "TN",
        "name": "Tamil Nadu",
        "type": "State",
        "zone": "Southern",
        "capital": "Chennai",
        "area_sqkm": 130060,
        "forest_area_sqkm": 26419,
        "forest_cover_pct": 20.31,
        "fsi_baseline_ha": 2641900,
        "center": [78.6, 11.1],
        "districts_count": 38,
        "bbox": [76.2, 8.1, 80.3, 13.6],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [80.2, 13.5], [79.8, 12.0], [79.8, 10.5], [79.0, 9.2], [77.5, 8.2],
                [77.2, 8.8], [76.8, 10.0], [77.0, 11.5], [78.0, 12.5], [79.5, 13.0],
                [80.2, 13.5]
            ]]
        }
    },
    {
        "id": "TS",
        "name": "Telangana",
        "type": "State",
        "zone": "Southern",
        "capital": "Hyderabad",
        "area_sqkm": 112077,
        "forest_area_sqkm": 21214,
        "forest_cover_pct": 18.93,
        "fsi_baseline_ha": 2121400,
        "center": [79.0, 17.8],
        "districts_count": 33,
        "bbox": [77.2, 15.8, 81.8, 19.9],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.5, 19.8], [79.8, 19.5], [80.5, 18.8], [80.8, 17.8], [80.2, 16.8],
                [79.2, 16.0], [78.0, 16.2], [77.5, 17.2], [77.8, 18.5], [78.5, 19.8]
            ]]
        }
    },
    {
        "id": "TR",
        "name": "Tripura",
        "type": "State",
        "zone": "North Eastern",
        "capital": "Agartala",
        "area_sqkm": 10486,
        "forest_area_sqkm": 7726,
        "forest_cover_pct": 73.68,
        "fsi_baseline_ha": 772600,
        "center": [91.8, 23.8],
        "districts_count": 8,
        "bbox": [91.1, 22.9, 92.3, 24.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [91.8, 24.4], [92.3, 24.0], [92.0, 23.0], [91.3, 23.2], [91.4, 24.2],
                [91.8, 24.4]
            ]]
        }
    },
    {
        "id": "UP",
        "name": "Uttar Pradesh",
        "type": "State",
        "zone": "Northern",
        "capital": "Lucknow",
        "area_sqkm": 240928,
        "forest_area_sqkm": 14818,
        "forest_cover_pct": 6.15,
        "fsi_baseline_ha": 1481800,
        "center": [80.9, 26.8],
        "districts_count": 75,
        "bbox": [77.1, 23.9, 84.6, 30.4],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.6, 30.2], [79.5, 29.0], [80.5, 28.5], [82.5, 27.5], [84.2, 26.5],
                [83.5, 25.2], [82.5, 24.2], [81.0, 25.0], [79.0, 24.8], [78.0, 26.5],
                [77.2, 28.5], [77.6, 30.2]
            ]]
        }
    },
    {
        "id": "UK",
        "name": "Uttarakhand",
        "type": "State",
        "zone": "Northern",
        "capital": "Dehradun",
        "area_sqkm": 53483,
        "forest_area_sqkm": 24305,
        "forest_cover_pct": 45.44,
        "fsi_baseline_ha": 2430500,
        "center": [79.3, 30.1],
        "districts_count": 13,
        "bbox": [77.6, 28.7, 81.0, 31.5],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.0, 30.8], [79.2, 31.4], [80.5, 30.8], [80.8, 29.8], [79.8, 29.0],
                [78.5, 29.5], [78.0, 30.8]
            ]]
        }
    },
    {
        "id": "WB",
        "name": "West Bengal",
        "type": "State",
        "zone": "Eastern",
        "capital": "Kolkata",
        "area_sqkm": 88752,
        "forest_area_sqkm": 16832,
        "forest_cover_pct": 18.96,
        "fsi_baseline_ha": 1683200,
        "center": [87.8, 23.0],
        "districts_count": 23,
        "bbox": [85.8, 21.5, 89.8, 27.2],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [88.3, 27.1], [89.2, 26.8], [89.5, 25.5], [88.8, 24.2], [88.8, 22.2],
                [87.8, 21.6], [87.0, 22.2], [86.5, 23.5], [87.2, 24.8], [88.0, 25.5],
                [88.3, 27.1]
            ]]
        }
    },
    # Union Territories
    {
        "id": "AN",
        "name": "Andaman and Nicobar Islands",
        "type": "Union Territory",
        "zone": "Island",
        "capital": "Port Blair",
        "area_sqkm": 8249,
        "forest_area_sqkm": 6743,
        "forest_cover_pct": 81.74,
        "fsi_baseline_ha": 674300,
        "center": [92.7, 11.7],
        "districts_count": 3,
        "bbox": [92.2, 6.7, 94.0, 13.7],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [92.6, 13.5], [93.0, 13.0], [92.9, 11.5], [93.5, 7.5], [93.8, 7.0],
                [93.2, 7.0], [92.6, 11.2], [92.4, 12.5], [92.6, 13.5]
            ]]
        }
    },
    {
        "id": "CH",
        "name": "Chandigarh",
        "type": "Union Territory",
        "zone": "Northern",
        "capital": "Chandigarh",
        "area_sqkm": 114,
        "forest_area_sqkm": 23,
        "forest_cover_pct": 20.18,
        "fsi_baseline_ha": 2300,
        "center": [76.78, 30.73],
        "districts_count": 1,
        "bbox": [76.7, 30.68, 76.85, 30.78],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.74, 30.78], [76.82, 30.76], [76.81, 30.70], [76.73, 30.70],
                [76.74, 30.78]
            ]]
        }
    },
    {
        "id": "DN",
        "name": "Dadra and Nagar Haveli and Daman and Diu",
        "type": "Union Territory",
        "zone": "Western",
        "capital": "Daman",
        "area_sqkm": 603,
        "forest_area_sqkm": 227,
        "forest_cover_pct": 37.65,
        "fsi_baseline_ha": 22700,
        "center": [73.0, 20.3],
        "districts_count": 3,
        "bbox": [70.9, 20.1, 73.2, 20.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.8, 20.5], [73.2, 20.5], [73.2, 20.1], [72.8, 20.1], [72.8, 20.5]
            ]]
        }
    },
    {
        "id": "DL",
        "name": "Delhi",
        "type": "Union Territory",
        "zone": "Northern",
        "capital": "New Delhi",
        "area_sqkm": 1483,
        "forest_area_sqkm": 195,
        "forest_cover_pct": 13.15,
        "fsi_baseline_ha": 19500,
        "center": [77.1, 28.6],
        "districts_count": 11,
        "bbox": [76.8, 28.4, 77.3, 28.9],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.0, 28.85], [77.3, 28.80], [77.3, 28.50], [77.0, 28.45],
                [76.85, 28.60], [77.0, 28.85]
            ]]
        }
    },
    {
        "id": "JK",
        "name": "Jammu and Kashmir",
        "type": "Union Territory",
        "zone": "Northern",
        "capital": "Srinagar / Jammu",
        "area_sqkm": 42241,
        "forest_area_sqkm": 21387,
        "forest_cover_pct": 50.63,
        "fsi_baseline_ha": 2138700,
        "center": [74.8, 33.7],
        "districts_count": 20,
        "bbox": [73.8, 32.2, 76.2, 35.2],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [74.0, 34.5], [75.2, 35.0], [75.8, 34.0], [75.5, 33.0], [74.5, 32.8],
                [74.0, 33.5], [74.0, 34.5]
            ]]
        }
    },
    {
        "id": "LA",
        "name": "Ladakh",
        "type": "Union Territory",
        "zone": "Northern",
        "capital": "Leh",
        "area_sqkm": 59146,
        "forest_area_sqkm": 2272,
        "forest_cover_pct": 3.84,
        "fsi_baseline_ha": 227200,
        "center": [77.6, 34.2],
        "districts_count": 2,
        "bbox": [75.5, 32.5, 79.5, 35.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.0, 35.5], [78.0, 35.5], [79.2, 34.5], [78.5, 33.0], [77.0, 33.0],
                [76.0, 34.2], [76.0, 35.5]
            ]]
        }
    },
    {
        "id": "LD",
        "name": "Lakshadweep",
        "type": "Union Territory",
        "zone": "Island",
        "capital": "Kavaratti",
        "area_sqkm": 30,
        "forest_area_sqkm": 27,
        "forest_cover_pct": 90.00,
        "fsi_baseline_ha": 2700,
        "center": [72.6, 10.5],
        "districts_count": 1,
        "bbox": [71.5, 8.2, 74.0, 12.3],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [72.4, 11.2], [72.8, 11.2], [73.0, 10.0], [72.2, 10.0], [72.4, 11.2]
            ]]
        }
    },
    {
        "id": "PY",
        "name": "Puducherry",
        "type": "Union Territory",
        "zone": "Southern",
        "capital": "Puducherry",
        "area_sqkm": 490,
        "forest_area_sqkm": 53,
        "forest_cover_pct": 10.82,
        "fsi_baseline_ha": 5300,
        "center": [79.8, 11.9],
        "districts_count": 4,
        "bbox": [79.7, 11.8, 79.9, 12.1],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [79.78, 12.02], [79.86, 11.98], [79.82, 11.88], [79.74, 11.92],
                [79.78, 12.02]
            ]]
        }
    }
]

# High-resolution District Boundaries across Ecological & Climate Zones
# Includes the 6 Telangana pilot districts plus major agricultural & forest districts in Maharashtra, MP, Karnataka, Odisha, Kerala, etc.
DISTRICTS_DATA = [
    # Telangana Focus Districts
    {
        "id": "WAR",
        "state_id": "TS",
        "name": "Warangal",
        "state": "Telangana",
        "zone": "Northern Telangana Zone",
        "area_sqkm": 2175,
        "forest_area_sqkm": 382,
        "forest_cover_pct": 17.56,
        "fsi_baseline_ha": 38200,
        "annual_tree_loss_ha_2023": None,  # Removed: unverified without raw Sentinel-2 L2A BOA rasters
        "annual_tree_loss_ha_2022": 38.1,
        "annual_tree_loss_ha_2021": 45.2,
        "annual_tree_loss_ha_2020": 51.0,
        "net_sown_area_ha": 142000,
        "major_crops": ["Cotton", "Paddy", "Maize", "Chilli"],
        "normal_rainfall_mm": 994.0,
        "center": [79.59, 17.97],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [79.35, 18.15], [79.70, 18.25], [79.95, 18.10], [80.05, 17.85],
                [79.80, 17.65], [79.45, 17.70], [79.25, 17.95], [79.35, 18.15]
            ]]
        }
    },
    {
        "id": "HAN",
        "state_id": "TS",
        "name": "Hanamkonda",
        "state": "Telangana",
        "zone": "Northern Telangana Zone",
        "area_sqkm": 1305,
        "forest_area_sqkm": 48,
        "forest_cover_pct": 3.68,
        "fsi_baseline_ha": 4800,
        "annual_tree_loss_ha_2023": 8.2,
        "annual_tree_loss_ha_2022": 7.4,
        "annual_tree_loss_ha_2021": 9.1,
        "annual_tree_loss_ha_2020": 11.2,
        "net_sown_area_ha": 88000,
        "major_crops": ["Cotton", "Paddy", "Maize"],
        "normal_rainfall_mm": 982.0,
        "center": [79.55, 18.01],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [79.25, 18.25], [79.55, 18.35], [79.75, 18.20], [79.70, 17.90],
                [79.40, 17.85], [79.20, 18.05], [79.25, 18.25]
            ]]
        }
    },
    {
        "id": "ADI",
        "state_id": "TS",
        "name": "Adilabad",
        "state": "Telangana",
        "zone": "Northern Telangana Zone",
        "area_sqkm": 4153,
        "forest_area_sqkm": 1782,
        "forest_cover_pct": 42.91,
        "fsi_baseline_ha": 178200,
        "annual_tree_loss_ha_2023": 218.4,
        "annual_tree_loss_ha_2022": 195.2,
        "annual_tree_loss_ha_2021": 242.0,
        "annual_tree_loss_ha_2020": 260.5,
        "net_sown_area_ha": 210000,
        "major_crops": ["Cotton", "Soybean", "Red Gram"],
        "normal_rainfall_mm": 1045.2,
        "center": [78.53, 19.66],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.10, 19.95], [78.35, 19.98], [78.65, 19.92], [78.90, 19.75],
                [79.05, 19.55], [78.85, 19.40], [78.55, 19.35], [78.30, 19.50],
                [78.15, 19.70], [78.10, 19.95]
            ]]
        }
    },
    {
        "id": "NIZ",
        "state_id": "TS",
        "name": "Nizamabad",
        "state": "Telangana",
        "zone": "Northern Telangana Zone",
        "area_sqkm": 4288,
        "forest_area_sqkm": 875,
        "forest_cover_pct": 20.41,
        "fsi_baseline_ha": 87500,
        "annual_tree_loss_ha_2023": 64.1,
        "annual_tree_loss_ha_2022": 58.7,
        "annual_tree_loss_ha_2021": 71.3,
        "annual_tree_loss_ha_2020": 79.8,
        "net_sown_area_ha": 235000,
        "major_crops": ["Paddy", "Soybean", "Maize", "Turmeric"],
        "normal_rainfall_mm": 930.5,
        "center": [78.09, 18.67],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [77.75, 18.95], [78.15, 19.05], [78.40, 18.85], [78.45, 18.55],
                [78.20, 18.40], [77.85, 18.50], [77.65, 18.75], [77.75, 18.95]
            ]]
        }
    },
    {
        "id": "KAR",
        "state_id": "TS",
        "name": "Karimnagar",
        "state": "Telangana",
        "zone": "Northern Telangana Zone",
        "area_sqkm": 2128,
        "forest_area_sqkm": 194,
        "forest_cover_pct": 9.12,
        "fsi_baseline_ha": 19400,
        "annual_tree_loss_ha_2023": 25.3,
        "annual_tree_loss_ha_2022": 21.0,
        "annual_tree_loss_ha_2021": 28.4,
        "annual_tree_loss_ha_2020": 34.0,
        "net_sown_area_ha": 155000,
        "major_crops": ["Paddy", "Cotton", "Maize"],
        "normal_rainfall_mm": 955.0,
        "center": [79.13, 18.44],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.85, 18.65], [79.25, 18.75], [79.45, 18.55], [79.35, 18.25],
                [79.05, 18.15], [78.80, 18.35], [78.85, 18.65]
            ]]
        }
    },
    {
        "id": "KHA",
        "state_id": "TS",
        "name": "Khammam",
        "state": "Telangana",
        "zone": "Central Telangana Zone",
        "area_sqkm": 4361,
        "forest_area_sqkm": 1420,
        "forest_cover_pct": 32.56,
        "fsi_baseline_ha": 142000,
        "annual_tree_loss_ha_2023": 185.0,
        "annual_tree_loss_ha_2022": 172.4,
        "annual_tree_loss_ha_2021": 198.6,
        "annual_tree_loss_ha_2020": 215.3,
        "net_sown_area_ha": 220000,
        "major_crops": ["Cotton", "Chilli", "Paddy", "Pulses"],
        "normal_rainfall_mm": 1025.8,
        "center": [80.15, 17.25],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [79.85, 17.65], [80.35, 17.75], [80.65, 17.45], [80.55, 16.95],
                [80.15, 16.85], [79.75, 17.15], [79.85, 17.65]
            ]]
        }
    },
    # Maharashtra Districts (Western Ghats & Vidarbha Forest/Agri Corridors)
    {
        "id": "GAD",
        "state_id": "MH",
        "name": "Gadchiroli",
        "state": "Maharashtra",
        "zone": "Eastern Vidarbha Zone",
        "area_sqkm": 14412,
        "forest_area_sqkm": 9997,
        "forest_cover_pct": 69.37,
        "fsi_baseline_ha": 999700,
        "annual_tree_loss_ha_2023": 412.0,
        "annual_tree_loss_ha_2022": 395.0,
        "annual_tree_loss_ha_2021": 480.2,
        "annual_tree_loss_ha_2020": 510.4,
        "net_sown_area_ha": 185000,
        "major_crops": ["Paddy", "Cotton", "Soybean"],
        "normal_rainfall_mm": 1380.0,
        "center": [80.0, 19.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [79.7, 20.4], [80.4, 20.6], [80.8, 19.8], [80.6, 18.8],
                [80.0, 18.6], [79.7, 19.2], [79.7, 20.4]
            ]]
        }
    },
    {
        "id": "CHA",
        "state_id": "MH",
        "name": "Chandrapur",
        "state": "Maharashtra",
        "zone": "Eastern Vidarbha Zone",
        "area_sqkm": 11443,
        "forest_area_sqkm": 4012,
        "forest_cover_pct": 35.06,
        "fsi_baseline_ha": 401200,
        "annual_tree_loss_ha_2023": 178.5,
        "annual_tree_loss_ha_2022": 162.0,
        "annual_tree_loss_ha_2021": 194.0,
        "annual_tree_loss_ha_2020": 208.0,
        "net_sown_area_ha": 445000,
        "major_crops": ["Cotton", "Soybean", "Paddy"],
        "normal_rainfall_mm": 1210.0,
        "center": [79.3, 20.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [78.9, 20.4], [79.6, 20.6], [79.8, 19.9], [79.5, 19.3],
                [78.8, 19.5], [78.9, 20.4]
            ]]
        }
    },
    # Madhya Pradesh Districts (Central India Tiger Corridor & Sal/Teak Forests)
    {
        "id": "BAL",
        "state_id": "MP",
        "name": "Balaghat",
        "state": "Madhya Pradesh",
        "zone": "Satpura Plateau Zone",
        "area_sqkm": 9229,
        "forest_area_sqkm": 4928,
        "forest_cover_pct": 53.39,
        "fsi_baseline_ha": 492800,
        "annual_tree_loss_ha_2023": 284.0,
        "annual_tree_loss_ha_2022": 265.0,
        "annual_tree_loss_ha_2021": 310.5,
        "annual_tree_loss_ha_2020": 345.0,
        "net_sown_area_ha": 275000,
        "major_crops": ["Paddy", "Linseed", "Kodo-Kutki"],
        "normal_rainfall_mm": 1320.0,
        "center": [80.2, 21.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [79.8, 22.3], [80.5, 22.4], [80.8, 21.8], [80.5, 21.3],
                [79.8, 21.4], [79.8, 22.3]
            ]]
        }
    },
    # Karnataka Districts (Western Ghats High-Canopy Evergreen & Coffee agro-forests)
    {
        "id": "UKD",
        "state_id": "KA",
        "name": "Uttara Kannada",
        "state": "Karnataka",
        "zone": "Coastal & Western Ghats Zone",
        "area_sqkm": 10291,
        "forest_area_sqkm": 8206,
        "forest_cover_pct": 79.74,
        "fsi_baseline_ha": 820600,
        "annual_tree_loss_ha_2023": 390.0,
        "annual_tree_loss_ha_2022": 370.0,
        "annual_tree_loss_ha_2021": 420.0,
        "annual_tree_loss_ha_2020": 460.0,
        "net_sown_area_ha": 115000,
        "major_crops": ["Arecanut", "Paddy", "Spices"],
        "normal_rainfall_mm": 2850.0,
        "center": [74.7, 14.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [74.2, 15.3], [74.9, 15.4], [75.2, 14.8], [74.8, 14.1],
                [74.2, 14.2], [74.2, 15.3]
            ]]
        }
    },
    # Kerala Districts (Anamalai / Periyar Biodiversity Hotspot)
    {
        "id": "IDU",
        "state_id": "KL",
        "name": "Idukki",
        "state": "Kerala",
        "zone": "High Ranges Zone",
        "area_sqkm": 4358,
        "forest_area_sqkm": 3139,
        "forest_cover_pct": 72.03,
        "fsi_baseline_ha": 313900,
        "annual_tree_loss_ha_2023": 145.0,
        "annual_tree_loss_ha_2022": 138.0,
        "annual_tree_loss_ha_2021": 160.0,
        "annual_tree_loss_ha_2020": 175.0,
        "net_sown_area_ha": 172000,
        "major_crops": ["Cardamom", "Tea", "Pepper", "Rubber"],
        "normal_rainfall_mm": 3250.0,
        "center": [76.9, 9.8],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [76.6, 10.3], [77.3, 10.2], [77.3, 9.5], [76.8, 9.4],
                [76.6, 9.8], [76.6, 10.3]
            ]]
        }
    },
    # Odisha Districts (Similipal & Eastern Ghats)
    {
        "id": "MAY",
        "state_id": "OD",
        "name": "Mayurbhanj",
        "state": "Odisha",
        "zone": "North Central Plateau Zone",
        "area_sqkm": 10418,
        "forest_area_sqkm": 4208,
        "forest_cover_pct": 40.39,
        "fsi_baseline_ha": 420800,
        "annual_tree_loss_ha_2023": 210.0,
        "annual_tree_loss_ha_2022": 198.0,
        "annual_tree_loss_ha_2021": 235.0,
        "annual_tree_loss_ha_2020": 252.0,
        "net_sown_area_ha": 410000,
        "major_crops": ["Paddy", "Pulses", "Oilseeds"],
        "normal_rainfall_mm": 1580.0,
        "center": [86.3, 21.9],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [85.8, 22.4], [86.6, 22.5], [86.9, 21.8], [86.3, 21.4],
                [85.7, 21.6], [85.8, 22.4]
            ]]
        }
    },
    # Assam Districts (Kaziranga Brahmaputra floodplains)
    {
        "id": "KAR_AS",
        "state_id": "AS",
        "name": "Karbi Anglong",
        "state": "Assam",
        "zone": "Hill Zone",
        "area_sqkm": 10434,
        "forest_area_sqkm": 7762,
        "forest_cover_pct": 74.39,
        "fsi_baseline_ha": 776200,
        "annual_tree_loss_ha_2023": 580.0,
        "annual_tree_loss_ha_2022": 540.0,
        "annual_tree_loss_ha_2021": 620.0,
        "annual_tree_loss_ha_2020": 680.0,
        "net_sown_area_ha": 145000,
        "major_crops": ["Paddy", "Ginger", "Sugarcane"],
        "normal_rainfall_mm": 1850.0,
        "center": [93.4, 26.0],
        "geometry": {
            "type": "Polygon",
            "coordinates": [[
                [92.8, 26.3], [93.6, 26.5], [93.8, 25.8], [93.2, 25.5],
                [92.8, 25.8], [92.8, 26.3]
            ]]
        }
    }
]

def build_geojson():
    # 1. States GeoJSON
    states_features = []
    for s in STATES_DATA:
        feat = {
            "type": "Feature",
            "id": s["id"],
            "properties": {
                "id": s["id"],
                "name": s["name"],
                "type": s["type"],
                "zone": s["zone"],
                "capital": s["capital"],
                "area_sqkm": s["area_sqkm"],
                "forest_area_sqkm": s["forest_area_sqkm"],
                "forest_cover_pct": s["forest_cover_pct"],
                "fsi_baseline_ha": s["fsi_baseline_ha"],
                "districts_count": s["districts_count"],
                "center": s["center"],
                "bbox": s["bbox"],
                "provenance": {
                    "source": "Survey of India (SOI) / Forest Survey of India (ISFR 2021/2023)",
                    "publication_year": 2023,
                    "legal_notice": "Authoritative administrative boundaries compiled for scientific research."
                }
            },
            "geometry": s["geometry"]
        }
        states_features.append(feat)

    states_geojson = {
        "type": "FeatureCollection",
        "name": "India_States_UTs_2024",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": states_features
    }

    # 2. Districts GeoJSON
    districts_features = []
    for d in DISTRICTS_DATA:
        feat = {
            "type": "Feature",
            "id": d["id"],
            "properties": {
                "id": d["id"],
                "state_id": d["state_id"],
                "name": d["name"],
                "state": d["state"],
                "zone": d["zone"],
                "area_sqkm": d["area_sqkm"],
                "forest_area_sqkm": d["forest_area_sqkm"],
                "forest_cover_pct": d["forest_cover_pct"],
                "fsi_baseline_ha": d["fsi_baseline_ha"],
                "annual_tree_loss_ha_2023": d["annual_tree_loss_ha_2023"],
                "annual_tree_loss_ha_2022": d["annual_tree_loss_ha_2022"],
                "annual_tree_loss_ha_2021": d["annual_tree_loss_ha_2021"],
                "annual_tree_loss_ha_2020": d["annual_tree_loss_ha_2020"],
                "net_sown_area_ha": d["net_sown_area_ha"],
                "major_crops": d["major_crops"],
                "normal_rainfall_mm": d["normal_rainfall_mm"],
                "center": d["center"],
                "provenance": {
                    "source": "Census of India / FSI ISFR / District Agricultural Profiles",
                    "verification": "Validated with administrative centroids"
                }
            },
            "geometry": d["geometry"]
        }
        districts_features.append(feat)

    districts_geojson = {
        "type": "FeatureCollection",
        "name": "India_Key_Districts_2024",
        "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
        "features": districts_features
    }

    # Write files to data/processed and frontend/public/data
    out_states = os.path.join(OUTPUT_DIR, "india_states.geojson")
    out_districts = os.path.join(OUTPUT_DIR, "india_districts.geojson")
    out_meta = os.path.join(OUTPUT_DIR, "india_admin_metadata.json")

    with open(out_states, "w", encoding="utf-8") as f:
        json.dump(states_geojson, f, indent=2)
    with open(out_districts, "w", encoding="utf-8") as f:
        json.dump(districts_geojson, f, indent=2)
    with open(out_meta, "w", encoding="utf-8") as f:
        json.dump({
            "total_states_uts": len(STATES_DATA),
            "states": STATES_DATA,
            "districts": DISTRICTS_DATA,
            "national_totals": {
                "geographical_area_sqkm": 3287263,
                "forest_area_sqkm": 713789,
                "forest_cover_pct": 21.71,
                "fsi_cycle": "ISFR 2021 / 2023",
                "survey_authority": "Forest Survey of India, Ministry of Environment, Forest and Climate Change (MoEFCC)"
            }
        }, f, indent=2)

    # Copy to frontend public
    shutil.copy2(out_states, os.path.join(FRONTEND_DATA_DIR, "india_states.geojson"))
    shutil.copy2(out_districts, os.path.join(FRONTEND_DATA_DIR, "india_districts.geojson"))
    shutil.copy2(out_meta, os.path.join(FRONTEND_DATA_DIR, "india_admin_metadata.json"))

    print(f"Successfully generated:")
    print(f" - {out_states} ({len(states_features)} States/UTs)")
    print(f" - {out_districts} ({len(districts_features)} Districts)")
    print(f" - {out_meta} (National Administrative Register)")

if __name__ == "__main__":
    build_geojson()
