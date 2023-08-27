# Wikiart Framer

parallel python3 main.py ::: {1..100}

parallel --retries 3 python3 -m wikiart_framer ::: {1..100}

python3 -m wikiart_framer --help
