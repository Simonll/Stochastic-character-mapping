import argparse
import glob
import os
from typing import List

import pandas as pd


def wrapper(input_dir: str, pattern: str, output: str) -> bool:

    os.makedirs(
        os.path.dirname(output) + "/",
        exist_ok=True,
    )
    list_of_df: List[pd.DataFrame] = []
    list_of_files: List[str] = glob.glob(input_dir + pattern)
    for f in list_of_files:
        df: pd.DataFrame = pd.read_csv(f, sep="\t", index_col=0)
        list_of_df += [df]

    try:
        pd.concat(list_of_df, axis=0, ignore_index=False).to_csv(output, sep="\t")
    except Exception as e:
        print("something wrong concatenating and saving file %s" % str(e))
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="argument", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--pattern",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    wrapper(
        input_dir=args.input_dir,
        pattern=args.pattern,
        output=args.output,
    )
