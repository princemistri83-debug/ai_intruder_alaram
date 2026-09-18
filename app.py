import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="AI Intruder Alarm", page_icon="🚨")

st.title("🚨 AI Security & Intruder Alarm")
st.write("તમારા ફોનના કેમેરાથી રૂમનું લાઈવ મોનિટરિંગ કરો.")

# કંટ્રોલ બટન
run = st.checkbox("કેમેરા ચાલુ કરો (Start Monitoring)")

FRAME_WINDOW = st.image([])

if run:
    camera = cv2.VideoCapture(0)
    
    # પહેલો ફ્રેમ સેટ કરો
    ret, frame1 = camera.read()
    ret, frame2 = camera.read()

    while camera.isOpened():
        if not run:
            break
            
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False
        for contour in contours:
            if cv2.contourArea(contour) < 900:
                continue
            motion_detected = True
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 0, 255), 2)

        if motion_detected:
            st.error("🚨 ચેતવણી: હલનચલન (Motion) જણાયેલ છે!")
        else:
            st.success("✅ પરિસ્થિતિ સામાન્ય છે.")

        # Streamlit માં ફ્રેમ બતાવો
        frame_rgb = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame_rgb)

        frame1 = frame2
        ret, frame2 = camera.read()

    camera.release()
