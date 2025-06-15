import cv2
import mediapipe as mp
import pickle
import numpy as np

modle_dict = pickle.load(open('./model.p', 'rb'))
model = modle_dict['model']

cap = cv2.VideoCapture(2)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.1)

while True:

    data_aux = []
    ret, frame = cap.read()

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hands_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,
                hands_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style()
            )
        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x)
                data_aux.append(y)

        model.predict(np.asarray(data_aux))

        


    cv2.imshow('frame', frame)
    cv2.waitKey(25)



cap.release()
cv2.destroyAllWindows()
