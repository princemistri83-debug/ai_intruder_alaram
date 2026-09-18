import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.set_page_config(page_title="AI Intruder Alarm", page_icon="🚨")
st.title("🚨 AI Security & Intruder Alarm")
st.write("તમારા ફોનના કેમેરાથી રૂમનું લાઈવ મોનિટરિંગ કરો.")

class MotionDetector(VideoTransformerBase):
    def __init__(self):
        self.prev_frame = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        if self.prev_frame is None:
            self.prev_frame = blur
            return img

        diff = cv2.absdiff(self.prev_frame, blur)
        _, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        self.prev_frame = blur
        return img

webrtc_streamer(key="intruder-alarm", video_transformer_factory=MotionDetector)
