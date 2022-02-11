# bt-tool
A small Python script that extracts metadata from XML files provided by the German *Bundestag* and converts them to BibTeX. I wrote the program for my PhD thesis in order to import *Drucksachen* and *Plenarprotokolle* into a literature database, e.g. Zotero.

## Folder structure

- `xml`: Put the original XML files (obtained from https://www.bundestag.de/services/opendata) here
- `pdf`: Put corresponding PDF files (obtained from https://dip.bundestag.de/) *with their original file names* here
- `bib`: The script will put BibTeX files here
- `full-text`: The script will put extracted full texts here
- `in-db`: Put *renamed* PDF files here

## Usage
The program comes with a command-line user interface in German.


## Citation
If you use the program for your research, please cite:

- Schlerka, Sebastian Matthias. 2021. *Islamdebatten im Deutschen Bundestag 1990-2009. Eine Habitusanalyse zur Formierungsphase deutscher Islampolitik.* Wiesbaden: Springer VS.
