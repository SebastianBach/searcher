import os


def get_image_path(img: str) -> str:

    current_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_folder, "test_images", img)


def get_test_project() -> str:
    current_folder = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_folder, "test_project")


def get_clean_temp_folder() -> str:

    current_folder = os.path.dirname(os.path.abspath(__file__))
    temp_folder = os.path.join(current_folder, "temp")

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    else:
        files = os.listdir(temp_folder)
        for file in files:
            file_path = os.path.join(temp_folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    return temp_folder
