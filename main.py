from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2

class IPWebcamStreamApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        # Create a Button to start playing the video
        play_button = Button(text='Play Video')
        play_button.bind(on_press=self.play_video)
        self.layout.add_widget(play_button)
        # Create a Video widget
        self.video_widget = Video(source='', state='stop')
        self.layout.add_widget(self.video_widget)
        return self.layout

    def play_video(self, instance):
        ip_cam_url = 'http://192.168.1.43:8080/video'
        self.video_stream = open_ip_webcam_stream(ip_cam_url)
        Clock.schedule_interval(self.update_video, 1 / 30.0)  # Update at 30 fps

    def update_video(self, dt):
        ret, frame = self.video_stream.read()
        if ret:
            # Convert the frame to a texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.video_widget.texture = texture

    def on_stop(self):
        self.video_stream.release()

def open_ip_webcam_stream(ip_cam_url):
    # Open the video stream
    cap = cv2.VideoCapture(ip_cam_url)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return None
    print(f"Streaming from {ip_cam_url}")
    return cap

if __name__ == '__main__':
    IPWebcamStreamApp().run()
