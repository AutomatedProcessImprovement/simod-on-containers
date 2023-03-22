import argparse
import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import gridspec


def visualize_historical_stats(historical_stats_path: str):
    df = pd.read_csv(historical_stats_path)

    fig = plt.figure(tight_layout=True, figsize=(10, 20))
    gs = gridspec.GridSpec(7, 1)
    ax1 = fig.add_subplot(gs[0, :])
    ax2 = fig.add_subplot(gs[1, :])
    ax3 = fig.add_subplot(gs[2, :])
    ax4 = fig.add_subplot(gs[3, :])
    ax5 = fig.add_subplot(gs[4, :])
    ax6 = fig.add_subplot(gs[5, :])
    ax7 = fig.add_subplot(gs[6, :])

    x = df['Timestamp']
    x = (x - x[0]) / 60

    y = df['User Count']
    ax1.plot(x, y)
    ax1.set_title('User Count')
    ax1.set_xlabel('Timedelta, minutes')
    ax1.set_ylabel('Count')
    ax1.set_yticks([y.min(), y.max() // 2, y.max()])

    y_rps = df['Requests/s']
    ax2.plot(x, y_rps)
    ax2.set_title('Locust Request Rate')
    ax2.set_xlabel('Timedelta, minutes')
    ax2.set_ylabel('Requests/s')
    ax2.set_yticks([y_rps.min(), y_rps.mean(), y_rps.mean() + y_rps.std(), y_rps.max()])
    ax2.grid()

    y = df['Total Average Response Time']
    ax3.plot(x, y)
    ax3.set_title('Response Time, Total Average')
    ax3.set_xlabel('Timedelta, minutes')
    ax3.set_ylabel('Duration, ms')
    ax3.set_yticks([y.min(), y.mean(), y.mean() + y.std(), y.max()])
    ax3.grid()

    y = df['90%']
    ax4.plot(x, y)
    ax4.set_title('Response Time, 90th percentile')
    ax4.set_xlabel('Timedelta, minutes')
    ax4.set_ylabel('Duration, ms')
    ax4.set_yticks([y.min(), y.mean(), y.max()])

    y_rc = df['Total Request Count']
    ax5.plot(x, y_rc)
    ax5.set_title('Total Request Count')
    ax5.set_xlabel('Timedelta, minutes')
    ax5.set_ylabel('Count')
    ax5.set_yticks([y_rc.min(), y_rc.max()])
    ax5.grid()

    y = df['Failures/s']
    ax6.plot(x, y)
    ax6.set_title('Failures/s')
    ax6.set_xlabel('Timedelta, minutes')
    ax6.set_ylabel('Failures/s')
    ax6.set_yticks([y.min(), y.max()])
    ax6.grid()

    y = df['Total Failure Count']
    ax7.plot(x, y)
    ax7.set_title('Total Failure Count')
    ax7.set_xlabel('Timedelta, minutes')
    ax7.set_ylabel('Count')
    ax7.set_yticks([y.min(), y.max()])
    ax7.grid()

    fig.align_labels()

    output_path = historical_stats_path.replace('.csv', '.png')
    plt.savefig(output_path)


def find_historical_stats_files(directory: str, file_name: str = 'simod-http_stats_history.csv'):
    for root, dirs, files in os.walk(directory):
        if file_name in files:
            yield os.path.join(root, file_name)


def visualize_historical_stats_in_directory(directory: str):
    for historical_stats_path in find_historical_stats_files(directory):
        logging.info(f'Processing {historical_stats_path}')
        visualize_historical_stats(historical_stats_path)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument('directory', help='Directory to search for historical stats files')
    args = parser.parse_args()

    visualize_historical_stats_in_directory(args.directory)
