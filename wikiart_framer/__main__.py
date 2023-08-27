import sys
import typer
import wikiart_framer
import glob

app = typer.Typer()

@app.command()
def download_one_random():
    url = wikiart_framer.ottieni_arte()
    file = wikiart_framer.download_image(url)

    FILE_NAME = str(file.filename)
    FILE_PATH = str(file.path)

    screen_box = wikiart_framer.box.Box()
    screen_box.set_width(480)
    screen_box.set_height(234)

    print("Schermo - " + str(screen_box))

    if FILE_PATH != "":
        wikiart_framer.process_image(FILE_PATH, FILE_NAME, screen_box)
    else:
        print("Nessun persorso disponibile")

@app.command()
def download_many(number: int):
    # url = "https://www.wikiart.org/en/ivan-bilibin/sketch-for-the-opera-the-golden-cockerel-by-nikolai-rimsky-korsakov-1909-1"
    for lp in range(number):
        download_one_random()


@app.command()
def download_one(url: str):
    # url = "https://www.wikiart.org/en/ivan-bilibin/sketch-for-the-opera-the-golden-cockerel-by-nikolai-rimsky-korsakov-1909-1"
    file = wikiart_framer.download_image(url)

@app.command()
def process_all():

    screen_box = wikiart_framer.box.Box()
    screen_box.set_width(480)
    screen_box.set_height(234)

    wikiart_framer.process_downloaded(screen_box)

@app.command()
def process_one(file_name: str):
# filepath = "gallery-dl/wikiart/Theophile Steinlen/577287e3edc2cb388008a5ef_Ces Dames Lafforest  Original drawing.jpg"

    screen_box = wikiart_framer.box.Box()
    screen_box.set_width(480)
    screen_box.set_height(234)

    dir_path = r"./gallery-dl/wikiart/*/*.*"
    res = glob.glob(dir_path)

    done = False

    for filepath in res:
        filename = filepath.split("/")[-1]

        if(filename == file_name):
            done = True
            wikiart_framer.process_image(filepath, file_name, screen_box)

    if not done:
        print('Nessun persorso disponibile')

if __name__ == "__main__":
    app()
