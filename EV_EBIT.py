import requests
import pandas as pd

def search_intrinio():

    userid = 'ade8e577d812742fe407b58424954579'
    password = '926a6ee50dd8e8f73530f2766e54da67'

    metrics = {'ev':'enterprisevalue~lt~100000000000000', 'ebit':'ebit~gt~-999999999999999'}
                #'evtoebit':'evtoebit~lt~9999999999999'}

    metric_data_temp = {}
    metric_data = {}
    pages = {}
    for metric in metrics:
        metric_data_temp[metric] = requests.get('https://api.intrinio.com/securities/search',
            params={'page_number': 1, 'conditions': metrics[metric]}, auth=(userid, password))
        pages[metric] = metric_data_temp[metric].json()['total_pages']
        metric_data[metric] = []
        for page in range(0, pages[metric]):
            data_temp = requests.get('https://api.intrinio.com/securities/search',
                params={'page_number': page, 'conditions': metrics[metric]},
                auth=(userid, password)).json()['data']
            metric_data[metric] += data_temp

    df_ev = pd.DataFrame(metric_data['ev'])
    df_ebit = pd.DataFrame(metric_data['ebit'])
    #df_ev_ebit = pd.DataFrame(metric_data['evtoebit'])

    final_data = df_ev.merge(df_ebit)
    final_data['evtoebit'] = final_data['enterprisevalue']/final_data['ebit']
    return final_data
