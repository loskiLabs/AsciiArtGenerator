import cv2 as cv

class VideoSource:

    def openVid(self, path):

        video = cv.VideoCapture(path)
        if not video.isOpened():
            print("Error: Cannot open video!")
            exit()

        
        return video
    
    def read_frame(self, video):


        width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
        frame_count = int(video.get(cv.CAP_PROP_FRAME_COUNT))

        print(f"Size: {width}x{height}, Frames: {frame_count}")
        self.get_fps(video)
        self.close(video)
    
    def get_fps(self, video):
        fps = video.get(cv.CAP_PROP_FPS)
        print(f"FPS: {fps}")
              
        return fps
    
    def close(self, video):
        video.release();