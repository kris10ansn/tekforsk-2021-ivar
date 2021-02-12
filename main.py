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

    text = []
    for region in results.regions:
        region_text = ""

        for line in region.lines:
            line_text = ""
            for word in line.words:
                line_text += " " + word

            region_text += line_text + "\n"

        text.append(region_text)

    return text


def capture_image():
    path = "./data/" + str(datetime.utcnow()) + ".png"
    with picamera.PiCamera() as camera:
        camera.capture(path)

    return path


def capture():
    image = capture_image()
    text = recognize_text(image)
    print(text)


capture()
