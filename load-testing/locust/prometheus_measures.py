import pandas as pd
import requests

prometheus_url = 'http://localhost:9090/api/v1/query'
time_range = '1h'


def main():
    df = get_simod_jobs_duration_df()
    df.to_csv('simod_jobs_duration.csv', index=False)

    # sum(simod_jobs_gauge) by(status)
    # df = get_simod_jobs_count_df()
    # df.to_csv('simod_jobs_count.csv', index=False)

    # kube_job_status_succeeded{job_name=~"simod.*"}[6h]
    response = fetch_query(query='kube_job_status_succeeded{job_name=~"simod.*"}[6h]')

    df = pd.DataFrame()
    for result in response['data']['result']:
        metric_name = result['metric']['__name__']
        job_name = result['metric']['job_name']
        timestamped_values = result['values']
        for timestamped_value in timestamped_values:
            timestamp = timestamped_value[0]
            value = timestamped_value[1]
            df = pd.concat([df, pd.DataFrame({
                'metric_name': [metric_name],
                'job_name': [job_name],
                'timestamp': [timestamp],
                'value': [value],
            })])

    return


def get_simod_jobs_duration_df() -> pd.DataFrame:
    global prometheus_url, time_range

    df = pd.DataFrame(columns=['request_id', 'duration_seconds', 'status'])

    status = 'pending'
    df = add_simod_jobs_duration_to_df(df, prometheus_url, status, time_range)

    status = 'running'
    df = add_simod_jobs_duration_to_df(df, prometheus_url, status, time_range)

    return df


def add_simod_jobs_duration_to_df(df: pd.DataFrame, prometheus_url: str, status: str, time_range: str) -> pd.DataFrame:
    response = fetch_simod_jobs_duration(prometheus_url, status, time_range)

    if response['status'] == 'success':
        for result in response['data']['result']:
            request_id = result['metric']['request_id']
            duration_seconds = result['value'][1]
            df = pd.concat([df, pd.DataFrame({
                'request_id': [request_id],
                'duration_seconds': [duration_seconds],
                'status': [status],
            })])

    return df


def fetch_simod_jobs_duration(prometheus_url: str, status: str, time_range: str) -> dict:
    return requests.get(
        prometheus_url,
        params={
            'query': f'sum by(request_id) '
                     f'(sum_over_time(simod_jobs_duration_seconds_sum{{status="{status}"}}[{time_range}]))',
        },
    ).json()


def fetch_query(query: str) -> dict:
    global prometheus_url

    return requests.get(
        prometheus_url,
        params={
            'query': query,
        },
    ).json()


def process_response(response: dict, func: callable, df: pd.DataFrame) -> pd.DataFrame:
    if response['status'] == 'success':
        for result in response['data']['result']:
            df = func(result, df)

    return df


if __name__ == '__main__':
    main()
