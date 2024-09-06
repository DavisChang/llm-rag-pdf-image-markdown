# install requirements

```
$ pyenv install 3.11.3
$ pyenv shell 3.11.3
$ pip install -r requirements.txt

$ marker_single ./pdfs/test-pdf-2.pdf ./output
$ marker_single ../../assets/pdf/test-pdf.pdf ./output --langs zh --batch_multiplier 2 --max_pages 5

```