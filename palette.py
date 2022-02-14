#! /bin/python3

# Try to import external library
try:
    from colorthief import ColorThief
except ImportError:
    die("Module 'colorthief' is required to be installed")

import sys

class Result(object):
    def __init__(self, ok: bool, value: any) -> None:
        self.ok = ok
        self.value = value

def die(message: str) -> None:
    print(message)
    sys.exit(1)

def usage() -> None:
    print("Usage: image-palette -i IMAGE_PATH [-n COLOR_COUNT] [-h]")
    print("\t-i IMAGE_PATH: Specify the path to image")
    print("")
    print("\t-n COLOR_COUNT: Specify the number of colors to be extracted from the image in question")
    print("")
    print("\t-h: Print this help message")

    sys.exit(1)

def parse_arguments(
    arguments: list[str],
    specification: dict[str, bool],
    overwrite: bool = True
) -> Result:
    is_option = lambda arg: arg[0] == '-'

    expect_option_value = False
    objects = list()
    boolean_options = list()
    value_options = dict()
    current_value_option = str()

    for arg in arguments:
        if is_option(arg):
            if expect_option_value:
                # An option value was expected, but another option was provided instead
                return Result(False, current_value_option)
            elif arg in specification:
                # It's a boolean option
                if specification[arg]:
                    boolean_options.append(arg)
                else:
                    expect_option_value = True
                    current_value_option = arg
            else:
                # The current option was not specified in the given specification
                return Result(False, arg)
        else:
            if expect_option_value:
                if (current_value_option in value_options) and (not overwrite):
                    # An option was tried to be set more than one time
                    # and overwriting was disabled
                    return Result(False, current_value_option)
                else:
                    value_options[current_value_option] = arg
                    expect_option_value = False
            else:
                objects.append(arg)

    if expect_option_value:
        # An option value was expected, the list of arguments ended instead
        return Result(False, current_value_option)

    return Result(True, (objects, boolean_options, value_options))

def extract_colors(image_path: str, color_count: int):
    def rgb_to_hex_string(rgb_tuple: tuple[int]) -> str:
        r, g, b = rgb_tuple

        # 11 -> 0xB -> '0xB' -> 'B'
        convert = lambda i: str(hex(i))[2:]

        return f"#{convert(r)}{convert(g)}{convert(b)}"

    try:
        color_thief = ColorThief(image_path)
        palette = color_thief.get_palette(color_count=color_count)

        return [rgb_to_hex_string(color) for color in palette]
    except FileNotFoundError:
        raise FileNotFoundError
    except UndefinedImageError:
        raise UndefinedImageError

def get_color_count(value_options: dict[str, str]) -> Result:
    COLOR_COUNT_OPTION = '-n'

    if COLOR_COUNT_OPTION in value_options:
        try:
            return Result(True, int(value_options[COLOR_COUNT_OPTION]))
        except ValueError:
            return Result(False, "The value given to '-n' must be numeric")
    else:
        return Result(True, 3) # Default color count

def get_image_path(value_options: dict[str, str]) -> Result:
    IMAGE_PATH_OPTION = '-i'

    if IMAGE_PATH_OPTION in value_options:
        return Result(True, value_options[IMAGE_PATH_OPTION])
    else:
        return Result(False, "No image was provided in the arguments")

def main() -> None:
    options = sys.argv[1:]
    specification = {
        "-n": False,
        "-i": False,
    }

    # Parse the program arguments
    arguments = parse_arguments(options, specification, overwrite=False)

    if arguments.ok:
        _objects, boolean_options, value_options = arguments.value
    else:
        usage()

    if _objects != []:
        usage()

    for option in boolean_options:
        if option == "-h":
            usage()

    # Get color count from arguments
    color_count = get_color_count(value_options)

    if color_count.ok:
        color_count = color_count.value
    else:
        die(color_count.value)

    # Get image path from arguments
    image_path = get_image_path(value_options)

    if image_path.ok:
        image_path = image_path.value
    else:
        usage()

    # Extract the colors from the image in question
    try:
        colors = extract_colors(image_path, color_count)
    except FileNotFoundError as e:
        die(f"'{image_path}' could not be found")
    except UndefinedImageError as e:
        die(f"Image format in '{image_path}' could not be identified")

    for color in colors:
        print(color)

if __name__ == "__main__":
    main()
