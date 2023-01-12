"""
Opis:
    Program obsługujący aplikacje YouTube gestami.

Autorzy:
    Damian Kijańczuk s20154
    Szymon Ciemny    s21355

Obsługiwane gesty:
    Kciuk w górę - podgłaśnia wideo
    Kciuk w dół - wycisza wideo
    Otwarta ręka - zatrzymuje lub wznawia odtwarzanie
    Palec wskazujący w górę - włącz napisy

Przygotowanie środowiska:
    Oprócz języka Python, potrzebna takze będzie biblioteka OpenCV, MediaPipe, Keyboard oraz Time.
    Uruchamiano na wersji python 3.10

    pip install opencv-python
    pip install mediapipe
    pip3 install keyboard

Uruchomienie oraz instrukcja:
    W celu sterowania wideo z platformy YouTube należy wybrać dowolny film na tej platformie oraz upewnić się że fokus
    będzie na tym właśnie wideo np. kliknąć na wideo przed rozpoczęciem wykonywania gestów.
"""
import time
import cv2
import keyboard
import mediapipe as mp

class handTrack():

    cap = cv2.VideoCapture(0)
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils

    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.modelComplex, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    #Function processes the image to detect hands and draw landmarks on the image
    def handsFinder(self,image,draw=True):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imageRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(image, handLms, self.mpHands.HAND_CONNECTIONS)
        return image

    #Function finds the positions of the landmarks on the image and draw circles on the image at the positions of the landmarks
    def positionFinder(self, image, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            Hand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(Hand.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
            if draw:
                cv2.circle(image, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmlist

    #Turn up or turn down sound
    def thumbUp(self, lmlist):
        if len(lmlist) != 0:
            thumb = lmlist[4][2]
            thumb_mid = lmlist[3][2]
            index = lmlist[8][2]
            middle = lmlist[12][2]
            ring = lmlist[16][2]
            pinky = lmlist[20][2]

            if thumb < index and thumb < middle and thumb < ring and thumb < pinky and thumb < thumb_mid:
                keyboard.press_and_release('up')
                time.sleep(2)

            elif thumb > index and thumb > middle and thumb > ring and thumb > pinky and thumb > thumb_mid:
                keyboard.press_and_release('down')
                time.sleep(2)

    #Stop or start wideo
    def openHand(self, lmlist):
        if len(lmlist) != 0:
            thumb = lmlist[4][2]
            index = lmlist[8][2]
            middle = lmlist[12][2]
            ring = lmlist[16][2]
            pinky = lmlist[20][2]

            if pinky > index and pinky > middle and pinky > ring  and pinky < thumb:
                keyboard.press_and_release('space')
                time.sleep(2)

    #Show subtitles
    def indexUp(self, lmlist):
        if len(lmlist) != 0:
            thumb = lmlist[5][1]
            index_y = lmlist[8][2]
            index_x = lmlist[8][1]
            index_mid = lmlist[7][2]
            index_bot = lmlist[6][2]
            middle = lmlist[12][1]
            ring = lmlist[16][1]
            pinky = lmlist[20][1]

            if index_y < index_mid < index_bot and index_x > thumb and index_x > middle and index_x > ring and index_x > pinky:
                keyboard.press_and_release('c')
                time.sleep(2)

if __name__ == "__main__":
    #Create instance of caputerd video from default camera "0"
    cap = cv2.VideoCapture(0)
    tracker = handTrack()

    while True:
        success, image = cap.read()
        image = tracker.handsFinder(image)
        lmList = tracker.positionFinder(image)
        tracker.thumbUp(lmList)
        tracker.openHand(lmList)
        tracker.indexUp(lmList)

        if len(lmList) != 0:
            print(lmList[4])
        cv2.imshow("Video", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
