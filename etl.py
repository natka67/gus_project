import pandas as pd
import requests

api_key = '40e719ee-4329-472f-3e50-08dbfd522f69'
headers = {'X-ClientId': api_key}
page_size = 100

voivodeships = dict(pd.read_excel('voivodeships_poland.xlsx', dtype={'id': str})[['name', 'id']].values).values()
variables_dictionary = {
    'K12': {'G603': ['P3820']},

    'K48': {'G597': ['P3783',
                     'P3785',
                     'P3786',
                     'P3787',
                     'P3788']},

    'K11': {'G231': [],
            'G619': ['P3953']}
}
variables_details = dict(zip(pd.read_excel('details_variables.xlsx')['name'],
                             pd.read_excel('details_variables.xlsx', dtype={'id_x': str})['id_x']))

data_ids = ['747060', '747061', '747062', '747063', '747064', '747065', '747066', '747067', '747068', '747069']


class CustomAPIError(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        if self.status_code == 404:
            return "Kod 404: Żądany zasób nie został odnaleziony."
        elif self.status_code == 200:
            return "Liczba zwróconych rekordów wyniosła zero."
        elif self.status_code == 403:
            return "Kod 403: Dostęp do żądanego zasobu jest zabroniony."
        elif self.status_code == 412:
            return "Kod 412: Nie spełnione warunki wstępne."
        elif self.status_code == 429:
            return "Kod 429: Przekroczono limit żądań w określonym czasie."
        else:
            return f"Błąd API o kodzie statusu {self.status_code}"


def get_locations():
    ''' Function for one-time data load to get areas ids
        Saves the result to an Excel file named areas.xlsx '''
    # Get the total number of areas
    response = requests.get('https://bdl.stat.gov.pl/api/v1/units?format=json&page=0&page-size=30')

    if response.status_code != 200:
        raise CustomAPIError(response.status_code)
    total_records = int(response.json()['totalRecords'])
    areas = []
    page_amount = int(total_records / page_size) + 1

    # Get data from all pages
    for page_number in range(page_amount):
        url = f'https://bdl.stat.gov.pl/api/v1/units?format=json&page={page_number}&page-size={page_size}'
        response = requests.get(url)
        if response.status_code != 200:
            raise CustomAPIError(response.status_code)
        # print(response)
        areas.extend(response.json()['results'])
    areas_df = pd.DataFrame(areas)
    voivodeships_poland_names = [
        "DOLNOŚLĄSKIE",
        "KUJAWSKO-POMORSKIE",
        "LUBELSKIE",
        "LUBUSKIE",
        "ŁÓDZKIE",
        "MAŁOPOLSKIE",
        "MAZOWIECKIE",
        "OPOLSKIE",
        "PODKARPACKIE",
        "PODLASKIE",
        "POMORSKIE",
        "ŚLĄSKIE",
        "ŚWIĘTOKRZYSKIE",
        "WARMIŃSKO-MAZURSKIE",
        "WIELKOPOLSKIE",
        "ZACHODNIOPOMORSKIE"
    ]
    areas_df[areas_df['name'].isin(voivodeships_poland_names)].to_excel('voivodeships_poland.xlsx')
    areas_df.to_excel('areas.xlsx')


def get_available_data():
    """Function for one time data load , needed for defining variables_id dictionary"""

    url_areas = 'https://bdl.stat.gov.pl/api/v1/subjects?lang=pl&format=json&page=0&page-size=33'
    url_subarea_base = 'https://bdl.stat.gov.pl/api/v1/subjects?parent-id='  # add parrent id for success
    url_childeren_base = 'https://bdl.stat.gov.pl/api/v1/subjects?parent-id='
    print(requests.get(url_areas))

    main_areas = pd.DataFrame(
        requests.get(url_areas).json()['results'])  # pd.DataFrame(requests.get(url_areas)['results'])
    main_areas.to_excel('main_areas.xlsx')

    # get subareas for choosen areas
    subareas = []
    for id_key in variables_dictionary.keys():
        url_subarea = url_subarea_base + id_key
        subarea = requests.get(url_subarea).json()['results']
        subareas.extend(subarea)
    subareas = pd.DataFrame(subareas)
    subareas.to_excel('subareas.xlsx')

    children_id = [k for i in variables_dictionary.values() for k in list(i.keys())]
    children = []
    for child_id in children_id:
        url_children = url_childeren_base + child_id
        child = requests.get(url_children).json()['results']
        children.extend(child)
    children = pd.DataFrame(children)
    children.to_excel('children.xlsx')

    ids = [j for i in variables_dictionary.values() for k in i.values() for j in k]
    empty_df = pd.DataFrame()
    empty_df.to_excel('variables.xlsx', index=False)
    var_list = []
    for id in ids:
        url_variable = f'https://bdl.stat.gov.pl/api/v1/variables?subject-id={id}&year=2020&format=json'
        variable = requests.get(url_variable).json()['results']
        var_list.extend(variable)
        variable_df = pd.DataFrame(variable)
        with pd.ExcelWriter('variables.xlsx', engine='openpyxl', mode='a') as writer:
            variable_df.to_excel(writer, sheet_name=str(id), index=False)
    var_df = pd.DataFrame(var_list)
    merged = pd.merge(var_df, children, how='left', left_on='subjectId', right_on='id')
    merged['id_x'] = merged['id_x'].astype(str)
    merged = merged[
        (merged['subjectId'] == 'P3820') |
        ((merged['subjectId'] == 'P3953') & (merged['n1'] == 'ogółem')) |
        ((merged['n1'] == 'ogółem') & (merged['n2'] == 'ogółem'))]

    merged.loc[merged['name'].str.contains('wskaźniki'), 'name'] = merged['n1']
    merged['merged_column'] = merged.apply(
        lambda row: row['name'].capitalize() if row['measureUnitName'] == '-' else f"{row['name']} ({row['measureUnitName']})".capitalize() ,
        axis=1)
    merged = merged.drop(['name', 'measureUnitName'], axis=1)
    merged = merged.rename(columns={'merged_column': 'name'})

    merged.to_excel('details_variables.xlsx')


def get_dataset(voivodeships_poland=voivodeships, variables_dict=variables_details, year='2020'):
    """Function to fetch data from an API for specified years"""
    variable_values = []
    for voivodeship in voivodeships_poland:
        row_data = {'Location': None, 'Year': None, 'Unit Measure': None, 'Key': None}

        for var_name, var_id in variables_dict.items():
            url_data_base = f'https://bdl.stat.gov.pl/api/v1/data/by-unit/{voivodeship}?format=json&var-id={var_id}&year={year}'
            response = requests.get(url_data_base, headers=headers)
            if response.status_code != 200 or response.json()['totalRecords'] == 0:
                raise CustomAPIError(response.status_code)

            data = response.json()['results'][0]
            row_data.update({str(var_name): data['values'][0]['val']})

            if row_data['Location'] is None:
                row_data['Location'] = response.json()['unitName']
                row_data['Year'] = data['values'][0]['year']
                row_data['Key'] = data['values'][0]['year'] + response.json()['unitName']

        variable_values.append(pd.DataFrame([row_data]))

    result_df = pd.concat(variable_values, ignore_index=True)

    return result_df
