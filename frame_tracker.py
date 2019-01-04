import cv2
import random


class FrameTracker:
    def __init__(self, video_path, count_manual=False):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)
        self.frame_count = 0
        if count_manual:
            # slow, but reliable
            self.total_frames = self._manual_count_total_frames()
        else:
            # fast, but unreliable
            self.total_frames = int(self.cap.get(7))

        # quick fix for none matching frame number
        self.last_frame = None
        self.end_of_frame = False

    def _manual_count_total_frames(self):
        '''Extremely slow, but accurate'''
        count = 0
        while self.cap.isOpened():
            ret, _ = self.cap.read()
            if ret is False:
                break

            count += 1
        
        self.set_frame_number(0)  # set frame to 0
        return count
    
    def __next__(self):
        '''Iterator'''
        if self.end_of_frame:
            # don't return frames until restarts
            return None
        else:
            frame = self.get_next_frame()
            self.frame_count += 1

            if self.frame_count >= self.total_frames:
                # next frame should loop back
                self.end_of_frame = True
                self.set_frame_number(0)  # set frame to index 0
            
            return frame

    def get_next_frame(self):
        ''''''
        ret, frame = self.cap.read()
        if not ret:
            print("Error: no frames available: ", self.video_path)
            return self.last_frame
        
        self.last_frame = frame
        return frame

    def set_frame_number(self, number):
        '''Set frame number'''
        self.cap.set(1, number)
        self.frame_count = number
        
    def is_end_of_frame(self):
        '''Indicates whether end of frame was achieved'''
        return self.end_of_frame

    def restart_env(self):
        '''Reset the environment so that we can get new frames'''
        self.end_of_frame = False

    def change_video(self, video_path):
        '''Change video for opencv capture'''
        self.cap = cv2.VideoCapture(video_path)
        self.total_frames = int(self.cap.get(7))

    def random_start(self):
        random_int = random.randint(0, self.total_frames-50)
        self.set_frame_number(random_int)

    def reset(self, video_path=None):
        '''Reset environment'''
        if video_path is not None:
            self.change_video(video_path)
        
        self.restart_env()

    def reset_with_random_start(self):
        '''reset the frame tracker with random start'''
        self.restart_env()
        self.random_start()

    def release(self):
        self.cap.release()

