import glob
import gallery_dl
import requests
from PIL import Image, ImageFilter

from . import box


def process_image(filepath: str, filename: str, screen_box: box.Box) -> None:
    """_summary_

    Args:
        filepath (str): _description_
        filename (str): _description_
        screen_box (box.Box): _description_
    """

    screen_box.scale(2)
    print("Schermo scalato - " + str(screen_box))

    cgratio = 14.0 / 225.0 * 2

    print("Opening file: " + filepath)

    # Apri immagine
    original_image = Image.open(filepath)

    image_box = box.Box()
    image_box.set_width(original_image.width)
    image_box.set_height(original_image.height)

    print("Immagine - " + str(image_box))

    scaled_box = box.Box()
    scaled_box.set_height(
        int(screen_box.get_height() - cgratio * screen_box.get_height())
    )
    scaled_box.set_width(int(screen_box.get_height() * image_box.get_ratio()))

    # Scala immagine
    ScaledImage = original_image.resize(scaled_box.cornerPoint.get_tuple())
    print("Immagine scalata - " + str(scaled_box))

    EhnancedImage = ScaledImage.convert("RGBA")

    BackgroudImage = original_image.copy()

    background_scaled_box = box.Box()
    background_scaled_box.set_width(screen_box.get_width())
    background_scaled_box.set_height(
        int(screen_box.get_width() / image_box.get_ratio())
    )

    ScaledBackgroudImage = BackgroudImage.resize(
        background_scaled_box.cornerPoint.get_tuple()
    )
    print("Background scalata - " + str(background_scaled_box))

    if (
        ScaledBackgroudImage.height < screen_box.get_height()
        or ScaledBackgroudImage.width < screen_box.get_width()
    ):
        print("Attenzione il background non copre tutto lo schermo")

    blurBackgroudImage = ScaledBackgroudImage.filter(ImageFilter.GaussianBlur(80))

    background_cut_box = box.Box()
    background_cut_box.set_y_offset(
        int((blurBackgroudImage.height - screen_box.get_height()) / 2)
    )
    background_cut_box.set_width(screen_box.get_width())
    background_cut_box.set_height(screen_box.get_height())

    cutBackgroudImage = blurBackgroudImage.crop(background_cut_box.get_tuple())
    print("Background tagliato - " + str(background_cut_box))

    # TODO: usere una box
    image_paste_box = box.Point()
    image_paste_box.x = int((cutBackgroudImage.width - EhnancedImage.width) / 2)
    image_paste_box.y = int((cutBackgroudImage.height - EhnancedImage.height) / 2)

    # TODO: fare setting per questo
    # aaa = makeShadow(EhnancedImage, 10, 10, (0, 0), 0xFFFFFF00, (0, 0, 0, 1))

    # Merge
    cutBackgroudImage.paste(EhnancedImage, image_paste_box.get_tuple())

    # cutBackgroudImage.show()
    # aaa.show()

    # TODO: parametrizzare cartella di uscita
    # Save blurImage
    cutBackgroudImage.save("archive/" + filename)


def download_image(url: str):
    """_summary_

    Args:
        url (_type_): _description_

    Returns:
        _type_: _description_
    """
    print("Inizio recupero immagini")

    job = gallery_dl.job.DownloadJob(url)
    code = job.run()

    # filepath = job.pathfmt.path
    # filename = job.pathfmt.filename

    print("Recupero file completato con codice: " + str(code))

    return job.pathfmt


def ottieni_arte() -> str:
    """_summary_

    Returns:
        str: _description_
    """

    wikiart_request = requests.get(
        "https://www.wikiart.org/en/App/Painting/random",
        allow_redirects=False,
        timeout=30,
    )

    url = "https://www.wikiart.org" + wikiart_request.headers.get("location")

    print("Nuova arte ottenuta. Url: " + url)

    return url


def makeShadow(image, iterations, border, offset, backgroundColour, shadowColour):
    """_summary_

    Args:
        image (_type_): base image to give a drop shadow
        iterations (_type_): number of times to apply the blur filter to the shadow
        border (_type_): border to give the image to leave space for the shadow
        offset (_type_): offset of the shadow as [x,y]
        backgroundColour (_type_): colour of the background
        shadowColour (_type_): colour of the drop shadow

    Returns:
        _type_: _description_
    """

    # Calculate the size of the shadow's image
    fullWidth = image.size[0] + abs(offset[0]) + 2 * border
    fullHeight = image.size[1] + abs(offset[1]) + 2 * border

    # Create the shadow's image. Match the parent image's mode.
    shadow = Image.new(image.mode, (fullWidth, fullHeight), backgroundColour)

    # Place the shadow, with the required offset
    shadowLeft = border + max(offset[0], 0)  # if <0, push the rest of the image right
    shadowTop = border + max(offset[1], 0)  # if <0, push the rest of the image down
    # Paste in the constant colour
    shadow.paste(
        shadowColour,
        [shadowLeft, shadowTop, shadowLeft + image.size[0], shadowTop + image.size[1]],
    )

    # Apply the BLUR filter repeatedly
    for i in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    # Paste the original image on top of the shadow
    imgLeft = border - min(offset[0], 0)  # if the shadow offset was <0, push right
    imgTop = border - min(offset[1], 0)  # if the shadow offset was <0, push down
    shadow.paste(image, (imgLeft, imgTop))

    return shadow


def process_downloaded(screen_box: box.Box):
    """_summary_"""

    dir_path = r"./gallery-dl/wikiart/*/*.*"
    res = glob.glob(dir_path)

    for filepath in res:
        filename = filepath.split("/")[-1]
        process_image(filepath, filename, screen_box)
