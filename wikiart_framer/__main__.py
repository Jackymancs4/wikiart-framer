import sys

if __package__ is None and not hasattr(sys, "frozen"):
    import os.path

    path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, os.path.realpath(path))

import wikiart_framer

wikiart_framer.box.Box()

if __name__ == "__main__":
    # sys.exit(gallery_dl.main())
    print("Ottengo nuova arte")
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
        sys.exit(0)
    else:
        print("Nessun persorso disponibile")

    sys.exit(1)


# print("Ottengo nuova arte")

# for lp in range(100):

# url = ottieniArte()
# url = "https://www.wikiart.org/en/ivan-bilibin/sketch-for-the-opera-the-golden-cockerel-by-nikolai-rimsky-korsakov-1909-1"
# file = downloadImage(url)

# processDownloaded()

# filepath = "gallery-dl/wikiart/Theophile Steinlen/577287e3edc2cb388008a5ef_Ces Dames Lafforest  Original drawing.jpg"
# filename = "test.jpg"

# filename = str(file.filename)
# filepath = str(file.path)

# if filepath != '':
#     processImage(filepath, filename)
# else:
#     print('Nessun persorso disponibile')
