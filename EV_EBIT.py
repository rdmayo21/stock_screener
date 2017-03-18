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


    '''
    for page in range(0, response_evtoebit_temp.json()['total_pages']):
        response_evtoebit = requests.get('https://api.intrinio.com/securities/search',
                                              params={'page_number': page + 1, 'conditions': 'evtoebit<100000'},
                                              auth=(userid, password))
        ev_ebit_data += response_evtoebit.json()['data']
    '''

    '''
    response_ebit = requests.get('https://api.intrinio.com/securities/search',
                                 params={'page_number': 1, 'conditions': ['ebit~gt~10']}, auth=(userid, password))
    response_mktcap = requests.get('https://api.intrinio.com/securities/search',
                                   params={'page_number': 1, 'conditions': ['marketcap~gt~1000000']},
                                   auth=(userid, password))
    response_ev = requests.get('https://api.intrinio.com/securities/search',
                               params={'page_number': 1, 'conditions': ['enterprisevalue~lt~1000000000000']},
                               auth=(userid, password))
    response_rev = requests.get('https://api.intrinio.com/securities/search',
                                params={'page_number': 1, 'conditions': ['totalrevenue~gt~1']}, auth=(userid, password))
    val_data_ebit = []
    val_data_mktcap = []
    val_data_ev = []
    val_data_rev = []

    for page in range(0, response_ebit.json()['total_pages']):
        response = requests.get('https://api.intrinio.com/securities/search',
                                params={'page_number': page + 1, 'conditions': ['ebit~gt~10']}, auth=(userid, password))

        print(response.status_code)
        val_data_ebit += response.json()['data']

    for page in range(0, response_mktcap.json()['total_pages']):
        response = requests.get('https://api.intrinio.com/securities/search',
                                params={'page_number': page + 1, 'conditions': ['marketcap~gt~1000000']},
                                auth=(userid, password))
        print(response.status_code)
        val_data_mktcap += response.json()['data']

    for page in range(0, response_ev.json()['total_pages']):
        response = requests.get('https://api.intrinio.com/securities/search',
                                params={'page_number': page + 1, 'conditions': ['enterprisevalue~lt~1000000000000']},
                                auth=(userid, password))
        print(response.status_code)
        val_data_ev += response.json()['data']

    for page in range(0, response_rev.json()['total_pages']):
        response = requests.get('https://api.intrinio.com/securities/search',
                                params={'page_number': page + 1, 'conditions': ['totalrevenue~gt~1']},
                                auth=(userid, password))
        print(response.status_code)
        val_data_rev += response.json()['data']

    '''

'''
val_sect = {}

for tick in merged_metrics[merged_metrics['ebit'] > 0].sort_values('ev/ebit').head(300)['ticker']:
    response_sect = requests.get('https://api.intrinio.com/companies?',
                                 params={'identifier': tick, 'page_number': 1, 'query': 'sector'},
                                 auth=(userid, password))
    val_sect[tick] = response_sect.json()['sector']

rev_df = pd.DataFrame(val_data_rev)
ebit_df_temp = pd.DataFrame(val_data_ebit)
ebit_df = ebit_df_temp[ebit_df_temp['ticker'].isin(rev_df['ticker'])]
mktcap_df_temp = pd.DataFrame(val_data_mktcap)
mktcap_df = mktcap_df_temp[mktcap_df_temp['ticker'].isin(rev_df['ticker'])]
ev_df_temp = pd.DataFrame(val_data_ev)
ev_df = ev_df_temp[ev_df_temp['ticker'].isin(rev_df['ticker'])]

merged_metrics = mktcap_df.merge(ebit_df).merge(ev_df).merge(rev_df)
merged_metrics['ev/ebit'] = merged_metrics['enterprisevalue'] / merged_metrics['ebit']
merged_metrics_300 = merged_metrics[merged_metrics['ebit'] > 0].sort_values('ev/ebit').head(300).merge(val_sect_df)
merge_metrics_final = merged_metrics_300[
    (merged_metrics_300['sector'] != 'Financial') & (merged_metrics_300['sector'] != 'Utilities')]
merge_metrics_final[20:80]
'''