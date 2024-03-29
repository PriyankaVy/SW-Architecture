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

set_choice = input("Choose the operation set (a/b/c): ")
if set_choice != 'a' and set_choice != 'b' and set_choice != 'c':
    print("Invalid operation set selected. Please choose 'a' or 'b' or 'c'.")
    exit()

if set_choice == "a":
    operations = [{"name": "flip", "axis": "vertical"},
                  {"name": "rotate", "degrees": 60},
                  {"name": "grayscale", "scale": "yes"},
                  {"name": "resize", "size": (2000, 2000)}]

    with open(filename, "rb") as handle:
        image_data = xmlrpc.client.Binary(handle.read())

    result = client.process_image(image_data, operations)
    processed_image_data = result.data

    with open("processed.jpg", "wb") as handle:
        handle.write(processed_image_data)

elif set_choice == "b":
    operations = [{"name": "rotate", "degrees": 40},
                  {"name": "flip", "axis": "horizontal"},
                  {"name": "resize", "size": (3000, 3000)},
                  {"name": "thumbnail"},
                  {"name": "grayscale", "scale": "yes"}]

    with open(filename, "rb") as handle:
        image_data = xmlrpc.client.Binary(handle.read())

    snapshot, final = client.process_image(image_data, operations)
    with open("thumbnail.jpg", "wb") as handle:
        handle.write(snapshot.data)
    with open("processed.jpg", "wb") as handle:
        handle.write(final.data)


elif set_choice == "c":
    operations = [{"name": "rotate", "degrees": 40},
                  {"name": "flip", "axis": "horizontal"},
                  {"name": "resize", "size": (3000, 3000)},
                  {"name": "thumbnail"},
                  {"name": "grayscale", "scale": "yes"},
                  {"name": "rotate_left_right", "side": "right"},
                  {"name": "resize", "size": (4000, 4000)},
                  {"name": "thumbnail"},
                  {"name": "resize", "size": (3000, 4000)},
                  {"name": "rotate_left_right", "side": "right"}]

    with open(filename, "rb") as handle:
        image_data = xmlrpc.client.Binary(handle.read())

    snapshot, final = client.process_image(image_data, operations)
    with open("thumbnail.jpg", "wb") as handle:
        handle.write(snapshot.data)
    with open("processed.jpg", "wb") as handle:
        handle.write(final.data)
