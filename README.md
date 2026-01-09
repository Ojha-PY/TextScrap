Below is a **clean, user-friendly, emoji-rich `README.md`** that explains **what the code does, how it works, and how to use it**, without overwhelming the reader.
It’s written so **both GIS users and Python users** can follow it confidently.

---

# 🧠✨ Neural Text Discovery from GeoTIFF

### *AI-Powered OCR → Spatial Points (Shapefile)*

> 🚀 Extract **printed text from raster maps** and convert it into **accurately georeferenced point features** using **Deep Learning + GIS**.

---

## 📌 What This Script Does

This script scans a **GeoTIFF map image**, detects **printed text using AI (OCR)**, and exports:

✅ **Each detected text as a POINT geometry**
✅ **Text stored as an attribute**
✅ **Original spatial reference preserved**
✅ **Output saved as an ESRI Shapefile**

💡 Perfect for:

* Maps with place names
* Survey maps
* Scanned cadastral sheets
* Satellite / aerial imagery with labels

---

## 🔥 Key Features

✨ **AI-Based OCR (EasyOCR)**
⚡ **GPU Acceleration (CUDA supported)**
🧭 **Accurate georeferencing using raster transform**
📊 **Confidence-based filtering**
🎛️ **Beautiful live progress bar (Rich UI)**
🗺️ **CRS auto-detected or custom projection supported**

---

## 🛠️ Requirements

Make sure you have Python **3.8+** and install the following:

```bash
pip install torch easyocr rasterio geopandas shapely pandas rich numpy
```

🔹 **Optional (for GPU)**

* NVIDIA GPU
* CUDA installed
* Compatible PyTorch build

---

## 📂 Input & Output

### 📥 Input

* **GeoTIFF raster** (`.tif`)
* Optional `.prj` or reference raster for projection

### 📤 Output

* **Shapefile (`.shp`)**

  * Geometry: `POINT`
  * Attribute: extracted text

---

## ▶️ How to Run

### 🖥️ Basic Usage (CPU)

```bash
python name_scrap_test.py \
  --input map.tif \
  --output output/text_points.shp
```

---

### ⚡ GPU Accelerated (Recommended)

```bash
python name_scrap_test.py \
  --input map.tif \
  --output output/text_points.shp \
  --gpu_id 0
```

💡 GPU is auto-detected if available.

---

### 🎯 Set Confidence Threshold

```bash
--confidence 60
```

🔹 Only text with **≥60% confidence** will be exported.

---

### 🧭 Custom Projection (Optional)

```bash
--projection map.prj
```

or

```bash
--projection reference.tif
```

---

## 🧠 How It Works (Step-by-Step)

1️⃣ **GPU Isolation (Early Stage)**
Prevents CUDA conflicts and ensures clean GPU usage.

2️⃣ **Raster Loading**
Reads the GeoTIFF and extracts:

* Pixel values
* Affine transform
* CRS

3️⃣ **AI OCR Scan**
EasyOCR detects text + bounding boxes.

4️⃣ **Pixel → Map Coordinate Conversion**
Each text bounding box center is converted to **real-world coordinates**.

5️⃣ **Confidence Filtering**
Low-confidence detections are discarded.

6️⃣ **Live Progress UI**
Beautiful real-time progress bar + detected text preview.

7️⃣ **Shapefile Export**
All valid text is written as spatial POINT features.

---

## 🧪 Output Example

| values       | geometry (POINT) |
| ------------ | ---------------- |
| Village Name | POINT (x y)      |
| Road No 12   | POINT (x y)      |
| School       | POINT (x y)      |

---

## ⚠️ Notes & Tips

⚠️ Works best with **printed text**, not handwriting
⚠️ Input raster should be **clear & high-resolution**
⚠️ For scanned maps, try increasing contrast beforehand
⚠️ GPU greatly improves speed on large rasters

---

## 👨‍💻 Author

**Muktikanta Ojha 😎**
Vision Intelligence Unit v2.5

---

## 📄 License

Free to use for **research, GIS automation, and learning**.
Modify responsibly.

---

## ⭐ Final Advice (Mentor Note)

If your raster is messy or low-resolution, **OCR will struggle**—that’s physics, not AI.
Clean input = clean output.
Get that right, and this pipeline is rock-solid.

---


