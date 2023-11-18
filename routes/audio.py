from fastapi import APIRouter, Body, UploadFile, File
from fastapi.responses import FileResponse
from deep.uitls import read_audio_to_wavform, predict
from models.audio import ResponseAudio, RequestAudio, Predictions
import tensorflow as tf
import datetime
import time
import os
import base64
from database.database import add_predictions, retrieve_predictions, retrieve_prediction, delete_prediction, PydanticObjectId

router = APIRouter()

model = tf.saved_model.load(r'\audio-cls-app\deep\models')

@router.post("/v1/predict", response_description="Audio classify", response_model=ResponseAudio)
async def audio_classify(file: UploadFile):
    print(file.content_type)
    if file.content_type != 'audio/wav':
        return {
            "status_code": 400,
            "response_type": "error",
            "description": "Invalid file format. Please upload a WAV file.",
            "data": {}
        }

    # Save the uploaded WAV file to a temporary directory
    folder =  str(datetime.datetime.now().strftime('%m-%d-%Y'))
    audio_name = str(datetime.datetime.now().strftime('%H-%M-%S')) +  '.wav' 
    audio_dir = 'public/audios/' + folder
    os.makedirs(audio_dir, exist_ok=True)
    audio_path = os.path.join(audio_dir, audio_name)
    
    with open(audio_path, "wb") as audio_file:
        audio_file.write(file.file.read())

    # Read the saved WAV file and perform prediction
    waveform = read_audio_to_wavform(audio_path)
    start_time = time.time()
    prediction = predict(model, waveform)
    end_time = time.time()

    # os.remove(audio_path)

    prediction_data = {
        'class_ids': prediction['class_ids'].numpy().tolist()[0],
        'class_names': prediction['class_names'].numpy().tolist()[0],
        'predictions': round(prediction['predictions'].numpy().max().tolist(), 4),
        'inference_time': (end_time - start_time),
        'predicted_at': datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
        'file_path': audio_path,
        'yn': 1
    }
    

    prediction_data = Predictions(**prediction_data)
    new_pred = await add_predictions(prediction_data)

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Operation successful",
        "data": prediction_data
    }

@router.post("/v1/predict-base64", response_description="Audio classify", response_model=ResponseAudio)
async def audio_classify_base64(request: RequestAudio = Body(...)):
    # Decode the base64 audio data
    print(request)
    try:
        audio_bytes = base64.b64decode(request.audio_data)
    except Exception as e:
        return {
            "status_code": 400,
            "response_type": "error",
            "description": "Invalid base64 encoding: " + str(e),
            "data": {}
        }

    # Save the decoded audio to a temporary WAV file
    folder =  str(datetime.datetime.now().strftime('%m-%d-%Y'))
    audio_name = str(datetime.datetime.now().strftime('%H-%M-%S')) +  '.wav' 
    audio_dir = 'public/audios/' + folder
    os.makedirs(audio_dir, exist_ok=True)
    audio_path = os.path.join(audio_dir, audio_name)
    with open(audio_path, "wb") as audio_file:
        audio_file.write(audio_bytes)

    # Read the saved WAV file and perform prediction
    waveform = read_audio_to_wavform(audio_path)
    start_time = time.time()
    prediction = predict(model, waveform)
    end_time = time.time()

    # Remove the temporary audio file
    # os.remove(audio_path)

    # Convert TensorFlow tensors to Python types
    prediction_data = {
        'class_ids': prediction['class_ids'].numpy().tolist()[0],
        'class_names': prediction['class_names'].numpy().tolist()[0].decode(),
        'predictions': round(prediction['predictions'].numpy().max().tolist(), 4),
        'inference_time': (end_time - start_time),
        'predicted_at': datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'),
        'file_path': audio_path,
        'yn': 1
    }
    
    prediction_data = Predictions(**prediction_data)
    new_pred = await add_predictions(prediction_data)

    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Operation successful",
        "data": prediction_data
    }
    
@router.get("/", response_description="Predictions retrieved", response_model=ResponseAudio)
async def get_predictions():
    predictions = await retrieve_predictions()
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Prediction data retrieved successfully",
        "data": predictions,
    }  

@router.get(
    "/{id}", response_description="Prediction data retrieved"
)
async def get_prediction(id: PydanticObjectId):
    prediction = await retrieve_prediction(id)
    if  prediction:
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "Prediction data retrieved successfully",
            "data": prediction,
        } 
         
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Prediction doesn't exist",
    }
   
   
@router.get(
    "/get-audio-file/{id}",
    response_description="Audio file retrieved"
)
async def get_audio_file(id: PydanticObjectId):
    prediction = await retrieve_prediction(id)

    if prediction and prediction.file_path:
        # Assuming prediction.file_path is the path to the audio file
        audio_file_path = prediction.file_path
        return FileResponse(audio_file_path, media_type="audio/mpeg")

    return {
        "status_code": 404,
        "response_type": "error",
        "description": "Audio file not found",
    }

