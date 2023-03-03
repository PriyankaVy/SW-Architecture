import xmlrpc.client

class ImageProcessorClient:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy('http://localhost:8000')

    def process_image(self, data, ops):
        return self.server.process_image(data, ops)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

client = ImageProcessorClient()

filename = input("Enter filename: ")
if not filename.lower().endswith(tuple(ALLOWED_EXTENSIONS)):
    print("Invalid file type. Allowed file types are: ", ALLOWED_EXTENSIONS)
    exit()

set_choice = input("Choose the operation set (a/b): ")
if set_choice != 'a' and set_choice != 'b':
    print("Invalid operation set selected. Please choose 'a' or 'b'.")
    exit()

if set_choice == "a":
    operations = [{"name": "flip", "axis": "vertical"},
                  {"name": "rotate", "degrees": 60},
                  {"name": "grayscale", "scale": "yes"},
                  {"name": "resize", "size": (1000, 1000)}]

    with open(filename, "rb") as handle:
        image_data = xmlrpc.client.Binary(handle.read())

    result = client.process_image(image_data, operations)
    processed_image_data = result.data

    with open("processed.jpg", "wb") as handle:
        handle.write(processed_image_data)

elif set_choice == "b":
    operations = [{"name": "rotate", "degrees": 40},
                  {"name": "flip", "axis": "horizontal"},
                  {"name": "thumbnail", "thumb": (300,300)},
                  {"name": "grayscale", "scale": "yes"},
                  {"name": "rotate_left_right", "side": "right"},
                  {"name": "thumbnail", "thumb": (300,300)},
                  {"name": "resize", "size": (800, 800)},
                  {"name": "rotate_left_right", "side": "right"}]

    with open(filename, "rb") as handle:
        image_data = xmlrpc.client.Binary(handle.read())

    snapshot, final = client.process_image(image_data, operations)
    with open("thumbnail.jpg", "wb") as handle:
        handle.write(snapshot.data)
    with open("processed.jpg", "wb") as handle:
        handle.write(final.data)
