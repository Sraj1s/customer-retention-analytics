.PHONY: install sample download full test clean

install:
	python -m pip install -r requirements.txt

sample:
	python -m src.run_pipeline --input data/sample/transactions_sample.csv

download:
	python -m src.download_data

full:
	python -m src.run_pipeline --input "data/raw/Online Retail.xlsx"

test:
	python -m pytest -q

clean:
	rm -f data/processed/*.csv data/processed/*.db reports/figures/*.png

