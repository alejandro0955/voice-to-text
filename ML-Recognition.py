import mediapipe as mp
import cv2
import os
import matplotlib.pyplot as plt
import pickle

data_dir = './asl_alphabet_train'
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.1)

print(os.listdir(data_dir))
data = []
labels = []
for dir in os.listdir(data_dir):
    for img_dir in os.listdir(os.path.join(data_dir,dir))[:500]:
        data_aux = []
        print(os.path.join(data_dir,dir,img_dir))
        img = cv2.imread(os.path.join(data_dir,dir,img_dir))
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_img)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
            if len(data_aux) == 42:
                data.append(data_aux)
                labels.append(dir)
            else:
                print("Not enough" + img_dir)
        # cv2.imshow("testts", rgb_img)
        # cv2.waitKey()

f = open('data.pickle', 'wb')
pickle.dump({'data': data, 'labels' : labels},f)
f.close()


