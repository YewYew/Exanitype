from PIL import Image, ImageFont, ImageDraw
import os

def create_image_from_text(input_text, image_folder):
    image_width = 0
    max_char_height = 0
    char_images = []

    for char in input_text:
        if char == " ":
            space_width = 70
            image_width += space_width
            char_images.append(Image.new("RGBA", (space_width, 0), (255, 255, 255, 0)))
        else:
            char_code = ord(char)
            if 65 <= char_code <= 90:
                char_image_path = os.path.join(image_folder, "0"+f"{char_code}.png")
                if os.path.exists(char_image_path):
                    char_image = Image.open(char_image_path)
                    char_images.append(char_image)
                    image_width += char_image.width
                    max_char_height = max(max_char_height, char_image.height)

    result_image = Image.new("RGBA", (image_width, max_char_height), (255, 255, 255, 0))
    x_offset = 0

    for char_image in char_images:
        y_offset = (max_char_height - char_image.height) // 2
        result_image.paste(char_image, (x_offset, y_offset), char_image)
        x_offset += char_image.width

    return result_image

user_input = input("Enter text (capital letters and spaces only): ")
image_folder = "title_font"
output_image = create_image_from_text(user_input, image_folder)
output_image.save("user_input.png")
