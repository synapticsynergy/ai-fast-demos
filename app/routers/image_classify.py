import os
from fastapi import FastAPI, Request, APIRouter, Depends, HTTPException, status, File, UploadFile
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models
import torch.nn as nn
import io
from typing import List, Dict

router = APIRouter()

# Device configuration
if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")

# Define the transform for inference
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# Load the model
def load_model(model_path, num_classes):
    model = models.resnet18(pretrained=False)
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.2),
        nn.Linear(num_ftrs, num_classes)
    )
    model.load_state_dict(torch.load(model_path, map_location=device))
    model = model.to(device)
    model.eval()
    return model

# Initialize model and class names
# Replace these with your actual values
MODEL_PATH = os.environ.get("IMAGE_CLASSIFY_MODEL_PATH")
IMAGE_CLASSES = os.environ.get("IMAGE_CLASSES")
class_names = sorted(IMAGE_CLASSES.split(","))
model = load_model(MODEL_PATH, len(class_names))


@router.get("/image_classes", tags=["image_classify"])
async def get_class_names():
    return {
        "class_names": class_names,
    }


@router.post("/classify_image", tags=["image_classify"])
async def predict(file: UploadFile = File(...)):
    # Read and transform the image
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data)).convert('RGB')
    image_tensor = transform(image).unsqueeze(0).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_class = class_names[predicted.item()]

    return {
        "predicted_class": predicted_class,
        "confidence_scores": torch.nn.functional.softmax(outputs[0], dim=0).tolist()
    }
