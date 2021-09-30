import re
from urllib.request import urlopen
from xml.etree.ElementTree import parse
# from mix_django.parse_xml import *
import pandas as pd

from product.models import Product, Characteristics, CharacteristicValue, Units


def parse_data_from_1s():
    xls = pd.ExcelFile(r"C:\Users\алексадр\PycharmProjects\mix_django\media\base.xls")
    sheetX = xls.parse(1)
    print(sheetX)
    print(sheetX['Артикул'])
    for key, i in pd.DataFrame(sheetX).iterrows():
        if not pd.isna(i['Артикул']):
            print(f"{i['Артикул']}-{i['Наименование']}")
            pr = Product(name=i['Наименование'], article=i['Артикул'], description=i['КОНТЕНТ'])
            pr.save()

def parse_data_weight():
    xls = pd.ExcelFile(r"C:\Users\алексадр\PycharmProjects\mix_django\media\base.xls")
    sheetX = xls.parse(3)
    print(sheetX)
    for key, i in pd.DataFrame(sheetX).iterrows():
        if not pd.isna(i['АРТИКУЛ']):
            print(f"{i['АРТИКУЛ']}-{i['Unnamed: 4']}")
            pr = Product.objects.filter(article=i['АРТИКУЛ']).first()
            if pr:
                pr.weight = float(i['Unnamed: 4'],)
                pr.save()

# from mix_django.parse_xml import *
def parse_data_characteristics():
    xls = pd.ExcelFile(r"C:\Users\алексадр\PycharmProjects\mix_django\media\bas2.xls")
    sheetX = xls.parse(1)
    print(sheetX)
    for key, i in pd.DataFrame(sheetX).iterrows():
        if not pd.isna(i['Unnamed: 1']):
            print(f"{i['Unnamed: 1']}-{i['Unnamed: 5']}")
            pr = Product.objects.filter(article=i['Unnamed: 1']).first()
            if pr:
                if isinstance(i['Unnamed: 5'], str):
                    charact = i['Unnamed: 5'].split('\n')
                    print(charact)
                    for ch in charact:
                        res = ch.split(':')
                        print(res)
                        if len(res)>=2:
                            unit = re.findall(r"\((.*?)\)", res[0])

                            if len(unit):
                                print(unit[0])
                                uu = Units.objects.filter(name=unit[0]).first()
                                if not uu:
                                    uu = Units(name=unit[0])
                                    uu.save()
                            else:
                                uu = Units.objects.filter(name="-").first()
                                if not uu:
                                    uu = Units(name="-")
                                    uu.save()
                            vvc = Characteristics.objects.filter(name=res[0]).first()
                            if not vvc:
                                vvc = Characteristics(name=res[0])
                                vvc.save()
                            vvb = CharacteristicValue.objects.filter(value=res[1]).first()
                            if not vvb:
                                vvb = CharacteristicValue(value=res[1], parent=vvc, units=uu)
                                vvb.save()
                                pr.characteristics.add(vvb)
                pr.save()
