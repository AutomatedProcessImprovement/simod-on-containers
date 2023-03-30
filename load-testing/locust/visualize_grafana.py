import argparse
import logging
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def visualize_amount_of_jobs(input_dir: Path):
    prefix = 'Amount of Jobs-data-'

    df = pd.DataFrame()

    for file_name in os.listdir(input_dir):
        if prefix not in file_name:
            continue

        df_ = pd.read_csv(str(input_dir / file_name))

        if df.empty:
            df = df_
            continue

        df = pd.merge(df, df_, on='Time', how='outer', sort=True)

    df = df.sort_values(by='Time')
    df.reset_index(inplace=True, drop=True)
    df = df.fillna(0)

    convert_time_column_to_timedelta(df, 'Time')

    plt.plot(df['Time'], df['failed'], label='failed')
    plt.plot(df['Time'], df['pending'], label='pending')
    plt.plot(df['Time'], df['running'], label='running')
    plt.plot(df['Time'], df['succeeded'], label='ducceeded')
    plt.title('Amount of Jobs')
    plt.xlabel('Timedelta, minutes')
    plt.ylabel('Count')
    plt.grid()
    plt.legend()

    output_path = input_dir / 'amount_of_jobs.png'
    plt.savefig(output_path)

    plt.clf()


def visualize_single_file(
        input_dir: Path,
        time_column: str = 'Time',
        value_column: str = 'avg(simod_jobs_duration_seconds_sum{status="pending"})',
        prefix: str = 'file-prefix',
        title: str = 'Plot Title',
        x_label: str = 'X Label',
        y_label: str = 'Y Label',
        grid: bool = True,
        legend: bool = False,
):
    for file_name in os.listdir(input_dir):
        if prefix not in file_name or Path(file_name).suffix != '.csv':
            continue

        df = pd.read_csv(str(input_dir / file_name))

        convert_time_column_to_timedelta(df, time_column)

        plt.plot(df[time_column], df[value_column])
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.grid(grid)
        if legend:
            plt.legend()

        output_path = input_dir / file_name.replace('.csv', '.png')
        plt.savefig(output_path)

        plt.clf()
        print(f'Output saved to {output_path}')
        break


def convert_time_column_to_timedelta(df: pd.DataFrame, time_column: str):
    df[time_column] = pd.to_datetime(df[time_column], unit='ms')
    df[time_column] = (df[time_column] - df[time_column][0]) / pd.Timedelta('1 minute')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path, help='Directory to with CSV files exported from Grafana')
    args = parser.parse_args()

    visualize_amount_of_jobs(args.directory)

    visualize_single_file(
        args.directory,
        prefix='Amount of Active Jobs (kube)-data-',
        title='Active Jobs',
        value_column='sum(kube_job_status_active)',
        x_label='Timedelta, minutes',
        y_label='Count',
        grid=True,
        legend=False,
    )

    visualize_single_file(
        args.directory,
        prefix='Jobs Failed (kube)-data-',
        title='Failed Jobs',
        value_column='sum(kube_job_status_failed)',
        x_label='Timedelta, minutes',
        y_label='Count',
        grid=True,
        legend=False,
    )

    visualize_single_file(
        args.directory,
        prefix='Job Processing Time-data-',
        title='Job Processing Time',
        value_column='avg(simod_jobs_duration_seconds_sum{status="running"})',
        x_label='Timedelta, minutes',
        y_label='Duration, seconds',
        grid=True,
        legend=False,
    )

    visualize_single_file(
        args.directory,
        prefix='Job Waiting Time-data-',
        title='Job Waiting Time',
        value_column='avg(simod_jobs_duration_seconds_sum{status="pending"})',
        x_label='Timedelta, minutes',
        y_label='Duration, seconds',
        grid=True,
        legend=False,
    )
