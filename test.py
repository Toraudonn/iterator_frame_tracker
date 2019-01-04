import sys
import cv2

from frame_tracker import FrameTracker


def main(fp=None, manual_count=False):
    if fp is None:
        return

    ft = FrameTracker(fp, manual_count)
    
    print(ft.total_frames)
    ft.set_frame_number(1780)
    
    while True:
        print(ft.frame_count)
        frame = next(ft)
        frame = cv2.resize(frame, (3840//4,1920//4))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if ft.is_end_of_frame():
            ft.reset_with_random_start()

    ft.release()


if __name__ == '__main__':
    fp = sys.argv[1]  # pass video 1st
    main(fp, False)

