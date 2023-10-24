# PyCom

Python Library & server-side API for accessing the PyCom database.

PyCom is an open-source, queryable database of Protein Residue-Residue Contacts (Coevolution Matrices) and annotation data derived from UniProt (Swiss-Prot to be precise!) using HHBlits/HHFilter/CCmpred.

More info can be found here:

[https://pycom.brunel.ac.uk/](https://pycom.brunel.ac.uk/)

It was primarly developed by me over the summers of 2022/2023. My work was financed by two grants by the Dept. of CompSci at Brunel University London.

## Archive

This repo was used during development and now serves as an archive. The main repo can be found at: [https://github.com/scdantu/pycom](https://github.com/scdantu/pycom)

The code for the creation of the database, that was deployed on the (Jade2)[https://www.jade.ac.uk/] HPC can be found at: [https://github.com/cemiu/pycom_generator](https://github.com/cemiu/pycom_generator)

## Installation

Install the PyCom library with:

`pip install git+https://github.com/scdantu/pycom`

Requirements:
- Python 3.8+
- numpy / pandas / h5py / requests, installed automatically

## Downloads

Get the `pycom.db` and `pycom.mat` files (**115 GB** total) from:

https://pycom.brunel.ac.uk/downloads/

**Not necessary** for remote use.


## Examples / Tutorials

### Local Use

Examples can be found in [example.ipynb](https://github.com/cemiu/pycom/blob/main/example.ipynb).
This requires the `pycom.db` and `pycom.mat` files.

### Remote Library

The library can be used remotely without downloading the `pycom.db` and `pycom.mat` files.
A tutorial can be found in [example_remote.ipynb](https://github.com/cemiu/pycom/blob/main/example.ipynb).

### API

It is also possible to use the API directly, hosted at https://pycom.brunel.ac.uk/api/.
