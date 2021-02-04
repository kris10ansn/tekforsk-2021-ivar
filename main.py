from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
from dotenv import load_dotenv
import os
import io
import time
import picamera
from datetime import datetime

load_dotenv()


def recognize_text(image_path):
    subscription_key = os.getenv("KEY")
    endpoint = os.getenv("ENDPOINT")

    client = ComputerVisionClient(
        endpoint, CognitiveServicesCredentials(subscription_key))

    image = open(image_path, "rb")
    results = client.recognize_printed_text_in_stream(image)

    for region in results.regions:
        for line in region.lines:
            for word in line.words:
                print(word.text)


def capture_image():
    path = "./data/" + str(datetime.utcnow()) + ".png"
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(5)
        camera.capture(path)

    return path


image_path = capture_image()
recognize_text(image_path)
