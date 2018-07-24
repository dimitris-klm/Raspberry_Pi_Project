import picamera
from time import sleep
import datetime
import base64

def take_picture():
    # First we need to take and save the picture
    with picamera.PiCamera() as camera:
        dt = datetime.datetime.now().strftime('%Y%m%d%H%M')
        camera.start_preview()
        sleep(1)
        camera.resolution = (640,480)
        full_image_path = '/home/pi/Shared/Image_On_' + dt + '.jpg'
        camera.capture(full_image_path,use_video_port=True)
        camera.stop_preview()
        sleep(0.5)
    # Now we encode the picture that we took to get the binary file

    image = open(full_image_path, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)

    return image_64_encode

if __name__ == "__main__":
    print "Taking picture"
    #print take_picture()
    print "Picture taken."
