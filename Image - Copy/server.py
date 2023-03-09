import xmlrpc.server
from io import BytesIO
from PIL import Image

class ImageProcessor:

    def __init__(self):
        pass

    def flip_image(self, image, axis):
        if axis == "horizontal":
            print("The image is flipped horizontally")
            return image.transpose(method=Image.FLIP_LEFT_RIGHT)
        elif axis == "vertical":
            print("The image is flipped vertically")
            return image.transpose(method=Image.FLIP_TOP_BOTTOM)
        elif axis == "no":
            return image

    def rotate_image(self, image, degrees):
        print("The image is rotated with " + str(degrees)+" degrees")
        return image.rotate(degrees)

    def grayscale_image(self, image, scale):
        if scale == "yes":
            print("The image is grayscaled ")
            return image.convert('L')
        elif scale == "no":
            return image

    def resize_image(self, image, size):
        print("The image is resized ")
        return image.resize(size)

    def thumbnail_image(self, image):
        print("The image thumbnail of 300*300 size is saved")
        thumb = 300, 300
        thumbnail_image = image.copy()
        thumbnail_image.thumbnail(thumb, resample=0)
        return thumbnail_image

    def rotate_left_right_image(self, image, side):
        if side == "left":
            print("The image is rotated left")
            return image.transpose(method=Image.ROTATE_90)
        elif side == "right":
            print("The image is rotated right")
            return image.transpose(method=Image.ROTATE_270)
        elif side == "no":
            return image

    def process_image(self, image_data, operations):
        image = Image.open(BytesIO(image_data.data))
        thumbnail = None

        if not operations:
            return image

        for op in operations:
            if op["name"] == "flip":
                image = self.flip_image(image, op["axis"])
                print(image.width, image.height)
            elif op["name"] == "rotate":
                image = self.rotate_image(image, op["degrees"])
                print(image.width, image.height)
            elif op["name"] == "grayscale":
                image = self.grayscale_image(image, op["scale"])
                print(image.width, image.height)
            elif op["name"] == "resize":
                image = self.resize_image(image, op["size"])
                print(image.width, image.height)
            elif op["name"] == "rotate_left_right":
                image = self.rotate_left_right_image(image, op["side"])
                print(image.width, image.height)
            elif op["name"] == "thumbnail":
                #thumbnail = image.copy()
                thumbnail = self.thumbnail_image(image)
                print(thumbnail.width, thumbnail.height)

        if thumbnail is not None:
            with BytesIO() as snap, BytesIO() as output:
                thumbnail.save(snap, format='JPEG')
                image.save(output, format='JPEG')
                return snap.getvalue(), output.getvalue()
        else:
            with BytesIO() as output:
                image.save(output, format='JPEG')
                return output.getvalue()

server = xmlrpc.server.SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
server.register_instance(ImageProcessor())
server.serve_forever()
