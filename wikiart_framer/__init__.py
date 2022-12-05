import gallery_dl
import requests
from PIL import Image, ImageFilter
import glob

from . import box


def processImage(filepath, filename):
    """Download images into appropriate directory/filename locations

    Args
    ----------
    filepath : str
        The file location of the spreadsheet
    filename : strs
        A flag used to print the columns to the console (default is
        False)
    """

    screen_width = 480 * 2
    screen_height = 234 * 2

    cgratio = 14.0 / 225.0 * 2
    screen_ratio = screen_width / screen_height

    print("Opening file: " + filepath)

    # Apri immagine
    OriImage = Image.open(filepath)

    image_ratio = OriImage.width / OriImage.height

    scaled_height = int(screen_height - cgratio * screen_height)
    scaled_width = int(scaled_height * image_ratio)

    # Scala immagine
    ScaledImage = OriImage.resize((scaled_width, scaled_height))
    print(
        "Immagine scalata. Larghezza: "
        + str(scaled_width)
        + " Altezza: "
        + str(scaled_height)
    )

    EhnancedImage = ScaledImage.convert("RGBA")

    BackgroudImage = OriImage.copy()

    background_scaled_width = int(screen_width)
    background_scaled_height = int(background_scaled_width / image_ratio)

    ScaledBackgroudImage = BackgroudImage.resize(
        (background_scaled_width, background_scaled_height)
    )
    print(
        "Background scalata. Larghezza: "
        + str(background_scaled_width)
        + " Altezza: "
        + str(background_scaled_height)
    )

    if (ScaledBackgroudImage.height < screen_height) or (
        ScaledBackgroudImage.width < screen_width
    ):
        print("Attenzione il background non copre tutto lo schermo")

    blurBackgroudImage = ScaledBackgroudImage.filter(ImageFilter.GaussianBlur(80))

    BackgroudCutBox = (
        0,
        int((blurBackgroudImage.height - screen_height) / 2),
        screen_width,
        int((blurBackgroudImage.height - screen_height) / 2) + screen_height,
    )

    cutBackgroudImage = blurBackgroudImage.crop(BackgroudCutBox)
    print(
        "Background tagliato. Larghezza: "
        + str(cutBackgroudImage.width)
        + " Altezza: "
        + str(cutBackgroudImage.height)
    )

    PasteImageBox = (
        int((cutBackgroudImage.width - EhnancedImage.width) / 2),
        int((cutBackgroudImage.height - EhnancedImage.height) / 2),
    )

    aaa = makeShadow(EhnancedImage, 10, 10, (0, 0), 0xFFFFFF00, (0, 0, 0, 1))

    # Merge
    cutBackgroudImage.paste(EhnancedImage, PasteImageBox)

    # cutBackgroudImage.show()
    # aaa.show()

    # Save blurImage
    cutBackgroudImage.save("archive/" + filename)


def downloadImage(url):

    print("Inizio recupero immagini")

    job = gallery_dl.job.DownloadJob(url)
    code = job.run()

    filepath = job.pathfmt.path
    filename = job.pathfmt.filename

    print("Recupero file completato con codice: " + str(code))

    return job.pathfmt


def ottieniArte():
    x = requests.get(
        "https://www.wikiart.org/en/App/Painting/random", allow_redirects=False
    )
    # print(x.status_code)
    # x = "test"

    url = "https://www.wikiart.org" + x.headers.get("location")

    print("Nuova arte ottenuta. Url: " + url)

    return url


def makeShadow(image, iterations, border, offset, backgroundColour, shadowColour):
    # image: base image to give a drop shadow
    # iterations: number of times to apply the blur filter to the shadow
    # border: border to give the image to leave space for the shadow
    # offset: offset of the shadow as [x,y]
    # backgroundCOlour: colour of the background
    # shadowColour: colour of the drop shadow

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


def processDownloaded():
    dir_path = r"./gallery-dl/wikiart/*/*.*"
    res = glob.glob(dir_path)

    for filepath in res:
        filename = filepath.split("/")[-1]
        processImage(filepath, filename)
