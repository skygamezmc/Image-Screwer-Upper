import math
import random
import time

from PIL import Image


def jpeg_to_hex(image_path):
    hex_colors = []

    # Open the image using Pillow
    image = Image.open(image_path)

    # Convert the image to RGB mode (to ensure it has three channels)
    image_rgb = image.convert("RGB")

    # Get the dimensions of the image
    width, height = image.size

    # Loop through every pixel and get the color value as a hex code
    for y in range(height):
        for x in range(width):
            r, g, b = image_rgb.getpixel((x, y))
            hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
            hex_colors.append(hex_color)

    return hex_colors

def get_image_dimensions(image_path):
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            return width, height
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)


# Replace 'path/to/your/image.jpg' with the actual path to your JPEG image file

def shuffle_list(hexcodes):
    random.shuffle(hexcodes)

def scramble_list(hexcodes):
    n = len(hexcodes)
    for i in range(n):
        j = random.randint(0, n - 1)
        hexcodes[i], hexcodes[j] = hexcodes[j], hexcodes[i]

def sort(hexcodes):
    # Define a function to convert hexcodes to integers
    def hex_to_int(hexcode):
        # Remove the '#' character if present, then convert to an integer
        return int(hexcode.lstrip('#'), 16)

    # Sort the list using the hex_to_int function as the key
    sorted_hexcodes = sorted(hexcodes, key=hex_to_int)

    return sorted_hexcodes

def reverse_list(hexcodes):
    hexcodes.reverse()

def duplicate_entries(hexcodes):
    # Choose a random number of times to duplicate the list (up to 5 times)
    num_duplicates = random.randint(1, 5)

    # Duplicate the list
    hexcodes *= num_duplicates

def remove_colors(hexcodes):
    # Choose a random number of colors to remove (up to half of the list length)
    num_colors_to_remove = random.randint(1, len(hexcodes) // 2)

    # Remove random colors from the list
    for _ in range(num_colors_to_remove):
        hexcodes.pop(random.randint(0, len(hexcodes) - 1))
    return hexcodes


# complex but round oclors loll

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(r, g, b)

def hex_to_rgb(hexcode):
    return tuple(int(hexcode.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

def quantize(value, levels):
    step = 256 / levels
    return int(value / step) * int(step)

def round_color_to_limit(hexcode, limit):
    r, g, b = hex_to_rgb(hexcode)
    levels = int(pow(limit, 1.0/3.0))  # Assuming a cubic root for RGB channels
    r = quantize(r, levels)
    g = quantize(g, levels)
    b = quantize(b, levels)
    return rgb_to_hex(r, g, b)

def round_hexcodes(hexcodes, color_limit):
    return [round_color_to_limit(hexcode, color_limit) for hexcode in hexcodes]

def hex_to_image(hex_colors, width, height, output_path):
    # Create a new image with the specified width and height
    image = Image.new("RGB", (width, height))

    # Loop through the hex_colors and set the pixel values in the image
    for y in range(height):
        for x in range(width):
            index = y * width + x
            if index < len(hex_colors):
                hex_color = hex_colors[index]
                rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
                image.putpixel((x, y), rgb_color)

    # Save the image to the specified output path
    image.save(output_path)


def compress_image(image_path, interim_path="temp_compressed.jpg", output_path="output_image.png", quality=5):
    """
    Compresses the image using the JPEG format and then saves it as a PNG.

    Args:
        image_path (str): Path to the input image.
        interim_path (str): Path to save the temporary compressed image.
        output_path (str): Path to save the final PNG image.
        quality (int): Quality setting for the JPEG compression. Ranges from 1 (worst) to 100 (best). Default is 5 which is quite compressed.
    """
    with Image.open(image_path) as img:
        img.save(interim_path, "JPEG", quality=quality)

    # Load the compressed JPEG and save it as PNG
    with Image.open(interim_path) as img:
        img.save(output_path, "PNG")

    # Optionally remove the temporary compressed JPG
    import os
    os.remove(interim_path)

def sine_hex(hex_codes, width, height, frequency, amplitude, effect):

    new_hexcodes = []

    for index, hex_code in enumerate(hex_codes):
        x_position = index % width
        y_position = index // width

        # Introducing a 2D wave component using both x and y
        spatial_frequency_x = math.sin(frequency * x_position / width)
        spatial_frequency_y = math.cos(frequency * y_position / height)

        # Combine the 2D wave patterns with time for a dynamic effect
        time_value = math.sin(time.time() + spatial_frequency_x + spatial_frequency_y)

        rgb = hex_to_rgb(hex_code)

        if effect == "brightness":
            # Modulate brightness with spatial variation
            modulated_rgb = tuple(clamp(int(value + amplitude * time_value * (x_position/width)), 0, 255) for value in rgb)
        elif effect == "contrast":
            # Modulate contrast with spatial variation
            contrast_factor = 1 + amplitude * time_value * (y_position/height)
            modulated_rgb = tuple(clamp(int(value * contrast_factor), 0, 255) for value in rgb)
        elif effect == "color_shift":
            # Modulate color shift with spatial variation
            r_shift = int(amplitude * time_value * (x_position/width))
            g_shift = int(amplitude * time_value * (y_position/height) * 0.5)
            b_shift = int(amplitude * time_value * ((width - x_position)/width) * -0.5)
            modulated_rgb = tuple(clamp(value + shift, 0, 255) for value, shift in zip(rgb, (r_shift, g_shift, b_shift)))
        else:
            modulated_rgb = rgb

        modulated_hex = rgb_to_hex(*modulated_rgb)
        new_hexcodes.append(modulated_hex)


    return new_hexcodes


def main():
    image_path = input("Enter input image: ")

    result_list = jpeg_to_hex(image_path)
    width, height = get_image_dimensions(image_path)

    print("Indexed")

    shuffle_or_sort = input("Choose action (shuffle, scramble, sort, reverse, duplicate, remove, limit, compress, sine): ")

    if shuffle_or_sort == "shuffle":
        shuffle_list(result_list)
    elif shuffle_or_sort == "scramble":
        scramble_list(result_list)
    elif shuffle_or_sort == "sort":
        result_list = sort(result_list)
    elif shuffle_or_sort == "reverse":
        reverse_list(result_list)
    elif shuffle_or_sort == "duplicate":
        duplicate_entries(result_list)
    elif shuffle_or_sort == "remove":
        result_list = remove_colors(result_list)
    elif shuffle_or_sort == "limit":
        color_limit = int(input("Enter the color limit (e.g. 256): "))  # Ask user for color limit
        result_list = round_hexcodes(result_list, color_limit)
    elif shuffle_or_sort == "compress":
        compress_image(image_path, output_path='output_image.png')

        print("done")
        return  # Exit the function here as we're done
    elif shuffle_or_sort == "sine":
        frequency = input("Enter sinewave frequency (default: 0.5):")
        amplitude = input("Enter sinewave amplitude (default: 127):")
        if frequency == "":
            frequency = 0.5
        else:
            frequency = float(frequency)

        if amplitude == "":
            amplitude = 127
        else:
            amplitude = float(amplitude)

        effect = input("Enter desired effect (brightness, contrast, color_shift): ")

        result_list = sine_hex(result_list, width, height, frequency, amplitude, effect)


    hex_to_image(result_list, width, height, 'output_image.png')
    print("done")

if __name__ == "__main__":
    main()


