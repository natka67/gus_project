from tkinter import *
import gui
import etl
import pandas as pd
import xlsxwriter

def create_ranking():


    data = etl.get_dataset()
    print(data)

