import logging
import argparse
import json
import os
from config import get_GP20UNIT1Gpc_config_from_path


def get_args_parser():
    parser = argparse.ArgumentParser(description='Get configuration for GP20UNIT1Gpc runs')
    parser.add_argument('--snap', type=int, help='Snapshot number')
    parser.add_argument('--path', type=str, help='Path to the hdf5 files')
    parser.add_argument('--output_path', type=str, help='Path to the output files')
    parser.add_argument('--ending', type=str, default=None, help='Ending of the hdf5 files')
    return parser


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    parser = get_args_parser()
    args = parser.parse_args()
    config = get_GP20UNIT1Gpc_config_from_path(args.snap, args.path, args.output_path, ending=args.ending)

    with open(os.path.join(args.output_path, 'config.json'), 'w') as f:
        json.dump(config, f, indent=4)

    logging.info(config)
