from typing import Optional, Any

from beanie import Document
from pydantic import BaseModel, EmailStr


class RequestAudio(BaseModel):
    audio_data: str  # Annotated attribute with type str

    class Config:
        json_schema_extra = {
            "example": {
                "audio_data": "Abdulazeez Abdulazeez Adeshina",
            }
        }

    class Settings:
        name = "audio"

class Predictions(Document):
    class_ids: int
    class_names: str
    predictions: float
    inference_time: float
    predicted_at: str
    file_path: str
    yn: int
    
    class Config:
        json_schema_extra = {
            "example": {
                'class_ids': 0,
                'class_names': 'Break',
                'predictions': 0.99,
                'inference_time': 0.1,
                'predicted_at': '11-05-2023 00:00:00',
                'file_path': '',
                'yn': 0        
            }
        }

    
    class Settings:  
        name = 'predictions'
        
class ResponseAudio(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": {
                    'class_ids': 0,
                    'class_names': 'Break',
                    'predictions': 0.99,
                    'inference_time': 0.1,
                    'predicted_at': '11-05-2023 00:00:00',
                    'file_path': '',
                    'yn': 0    
                },
            }
        }
