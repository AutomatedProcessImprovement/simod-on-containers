import argparse
import logging
import os
from pathlib import Path
from typing import Tuple, List, Optional

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec


def make_grid(rows: int, columns: int = 1, figsize: tuple = (10, 20)) -> Tuple[plt.Figure, List[plt.Axes]]:
    fig = plt.figure(tight_layout=True, figsize=figsize)
    gs = gridspec.GridSpec(rows, columns)
    axes = [fig.add_subplot(gs[i, :]) for i in range(rows)]
    return fig, axes


def visualize_amount_of_jobs(input_dir: Path, ax: Optional[plt.Axes] = None):
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

    if ax is None:
        fig, axes = make_grid(1, 1)
        ax = axes[0]

    if 'failed' in df.columns:
        ax.plot(df['Time'], df['failed'], label='failed', color='red')
    if 'pending' in df.columns:
        ax.plot(df['Time'], df['pending'], label='pending', color='orange')
    if 'running' in df.columns:
        ax.plot(df['Time'], df['running'], label='running', color='blue')
    if 'succeeded' in df.columns:
        ax.plot(df['Time'], df['succeeded'], label='succeeded', color='green')
    ax.set_title('Amount of Jobs')
    ax.set_xlabel('Timedelta, minutes')
    ax.set_ylabel('Count')

    ax.set_yticks([0, df['running'].max(), df['succeeded'].max(), df['pending'].max()])

    # x ticks starting from 0 and every 5 minutes and ending at the max value
    x_ticks = [0]
    x_ticks.extend(range(0, round(df['Time'].max()), 5))
    if x_ticks[-1] != round(df['Time'].max()):
        x_ticks.append(round(df['Time'].max()))
    ax.set_xticks(x_ticks)

    running_max_time = df[df['running'] == df['running'].max()]['Time'].values[0]
    succeeded_max_time = df[df['succeeded'] == df['succeeded'].max()]['Time'].values[0]

    ax.annotate(
        f'{df["running"].max()}',
        xy=(running_max_time, df['running'].max()),
        xytext=(running_max_time, df['running'].max()),
        arrowprops=dict(facecolor='blue', shrink=0.05),
    )

    ax.annotate(
        f'{df["succeeded"].max()}',
        xy=(succeeded_max_time, df['succeeded'].max()),
        xytext=(succeeded_max_time, df['succeeded'].max()),
        arrowprops=dict(facecolor='green', shrink=0.05),
    )

    ax.grid()
    ax.legend()

    if ax is None:
        output_path = input_dir / 'amount_of_jobs.png'
        plt.savefig(str(output_path))


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
        ax: Optional[plt.Axes] = None,
):
    for file_name in os.listdir(input_dir):
        if prefix not in file_name or Path(file_name).suffix != '.csv':
            continue

        df = pd.read_csv(str(input_dir / file_name))

        convert_time_column_to_timedelta(df, time_column)

        if ax is None:
            fig, axes = make_grid(1, 1)
            ax = axes[0]

        ax.plot(df[time_column], df[value_column])
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.grid(grid)
        if legend:
            ax.legend()

        if ax is None:
            output_path = input_dir / file_name.replace('.csv', '.png')
            plt.savefig(output_path)


def convert_time_column_to_timedelta(df: pd.DataFrame, time_column: str):
    df[time_column] = pd.to_datetime(df[time_column], unit='ms')
    df[time_column] = (df[time_column] - df[time_column][0]) / pd.Timedelta('1 minute')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path, help='Directory to with CSV files exported from Grafana')
    args = parser.parse_args()

    fig, axes = make_grid(4)

    visualize_amount_of_jobs(args.directory, ax=axes[0])

    # visualize_single_file(
    #     args.directory,
    #     prefix='Amount of Active Jobs (kube)-data-',
    #     title='Active Jobs',
    #     value_column='sum(kube_job_status_active)',
    #     x_label='Timedelta, minutes',
    #     y_label='Count',
    #     grid=True,
    #     legend=False,
    #     ax=axes[1],
    # )

    visualize_single_file(
        args.directory,
        prefix='Jobs Failed (kube)-data-',
        title='Failed Jobs',
        value_column='sum(kube_job_status_failed)',
        x_label='Timedelta, minutes',
        y_label='Count',
        grid=True,
        legend=False,
        ax=axes[1],
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
        ax=axes[2],
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
        ax=axes[3],
    )

    fig.align_ylabels(axes)

    output_path = args.directory / 'grafana_data.png'
    plt.savefig(str(output_path))
