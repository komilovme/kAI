from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pytesseract
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def root():
    return {"status": "OCR server is running"}

@app.post("/ocr")
async def ocr_image(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))

        text = pytesseract.image_to_string(image, lang="eng")

        return JSONResponse({
            "success": True,
            "text": text.strip()
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )
