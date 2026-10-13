#!/usr/bin/env python3
"""Convert 8 user-owned Cartline TOPDON hero WEBP images to compliant JPEGs.
Public assets for AUTODOC Mirakl image_1 P48 import; no product/offer changes.
"""
import io,json,urllib.request
from pathlib import Path
from PIL import Image,ImageOps
IMAGES={
"TAD900_BT":"https://cartline.de/wp-content/uploads/2026/06/AD900BT-1-1.webp",
"TAD_EU":"https://cartline.de/wp-content/uploads/2026/06/ArtiDiagEU_0.webp",
"TBT600":"https://cartline.de/wp-content/uploads/2026/06/BT600-_1.webp",
"TPELITE":"https://cartline.de/wp-content/uploads/2026/06/TD52110042_1.webp",
"TSLITE":"https://cartline.de/wp-content/uploads/2026/06/TopScan_Pro-0.webp",
"TSMASTER":"https://cartline.de/wp-content/uploads/2026/06/TopScan_Pro-0.webp",
"T4000":"https://cartline.de/wp-content/uploads/2026/06/Tornado40002023Version_1.webp",
"T90000":"https://cartline.de/wp-content/uploads/2026/06/BatteryChargerTornado9000001.webp"
}
dest=Path("public-assets/autodoc/topdon")
dest.mkdir(parents=True,exist_ok=True)
for ref,url in IMAGES.items():
 req=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0 (compatible; CartlineMediaOptimization/1.0)"})
 with urllib.request.urlopen(req,timeout=30) as response:
  if response.status!=200:raise SystemExit("SOURCE_HTTP_NOT_200:"+ref)
  data=response.read(3*1024*1024)
 pic=Image.open(io.BytesIO(data))
 pic.load()
 if pic.format.upper() not in ("WEBP","JPEG","PNG"):raise SystemExit("INVALID_SOURCE_FORMAT:"+ref)
 pic=ImageOps.exif_transpose(pic)
 if pic.width<300 or pic.height<300:raise SystemExit("ORIGINAL_RESOLUTION_TOO_LOW:"+ref)
 rgba=pic.convert("RGBA")
 white=Image.new("RGB",rgba.size,(255,255,255))
 white.paste(rgba,mask=rgba.getchannel("A"))
 target=dest/(ref.lower()+".jpg")
 for quality in (87,80,72,65):
  buffer=io.BytesIO()
  white.save(buffer,format="JPEG",quality=quality,optimize=True,progressive=True,subsampling=0)
  if buffer.tell()<485000:break
 else:raise SystemExit("IMAGE_TOO_LARGE:"+ref)
 target.write_bytes(buffer.getvalue())
 print("AUTODOC_JPEG="+json.dumps({"ref":ref,"source_bytes":len(data),"jpeg_bytes":target.stat().st_size,
  "resolution":[pic.width,pic.height],"format":"JPEG",
  "target":str(target)},ensure_ascii=False))
