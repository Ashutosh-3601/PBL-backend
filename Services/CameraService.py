import cv2
import time

class CameraService:
    def __init__(self, number, wait = 10):
        self.card = number
        self.delay = wait

    def capture(self):
        try:
            # Start the Camera
            vid = cv2.VideoCapture(0)
            # Current timestamp?
            now = time.time()

            while(True): 
                success, frame = vid.read()
                # COLOR FORMAT: BGR
                cv2.putText(frame, 'Adjust your face', (150, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.rectangle(frame, (125, 90), (500, 400), (0, 255, 0), 3)
                cv2.putText(frame, f'Capturing in {self.delay} seconds', (100, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
                cv2.imshow('FRAME', frame)

                # Get REGION OF INTEREST
                ROI = frame[90:90+310, 128:128+371]
                if cv2.waitKey(1) == ord('q'):
                    break;

                if time.time() - now > self.delay:
                    # Cache image?
                    cv2.imwrite(f'image/{self.card}.jpg', ROI)
                    break

            vid.release()
            cv2.destroyAllWindows()
            return True
        except:
            return False