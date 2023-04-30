import pandas as pd

csv = pd.read_csv('~/Downloads/zHV_aktuell_csv.2023-03-13.csv', delimiter= ';')
csv = csv[csv['Municipality'] == 'Hamburg']
csv_reduced = csv.drop(['SeqNo', 'Parent', 'MunicipalityCode', 'DistrictCode', 'District', 'Condition', 'State', 'Description', 	'Authority', 	'DelfiName', 	'TariffDHID', 	'TariffName', 'Municipality'], axis = 1)
csv_reduced = csv_reduced.sample(128)

csv_reduced.to_csv('data/hamburg_small.csv', sep=';')