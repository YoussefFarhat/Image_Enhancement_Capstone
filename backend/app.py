import io
from pathlib import Path

from PIL import Image
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse

from backend.model import ImageEnhancement

MODELS_PATH = Path(__file__).resolve().parent / "models"
PRETRAINED_MODEL_PATH = MODELS_PATH / "RealESRGAN_x4plus.pth"
model = ImageEnhancement(PRETRAINED_MODEL_PATH)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_PATH = PROJECT_ROOT / "frontend"

# FASTAPI


app = FastAPI(
    title="Image Quality Enhancement API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API ROUTES

@app.get("/")
@app.head("/")
def read_root():

    return FileResponse(
        FRONTEND_PATH / "index.html"
    )


@app.post("/enhance")
async def enhance(
    file: UploadFile = File(...)
):
    """
    Receive an image, enhance it using the
    pretrained Real-ESRGAN model twice,
    and return the enhanced PNG.
    """

    contents = await file.read()

    input_image = Image.open(
        io.BytesIO(contents)
    ).convert("RGB")

    output_image = model.enhance_image(
        input_image
    )

    buffer = io.BytesIO()

    output_image.save(
        buffer,
        format="PNG"
    )

    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="image/png"
    )