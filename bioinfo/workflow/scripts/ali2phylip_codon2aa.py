import argparse
import os

from bintools.align.align import ali
from bintools.align.align import read_phylip
from bintools.align.align import write_phylip


def codon2aa(input: str, phylip: str) -> bool:
    try:
        os.makedirs(os.path.dirname(phylip), exist_ok=True)
    except Exception as e:
        print(
            "somehting wrong when making dir %s, %s" % (os.path.dirname(phylip), str(e))
        )
        return False
    try:
        with open(input, "r") as fh:
            ali_: ali = read_phylip(fh=fh)
            write_phylip(
                filename=phylip,
                align=ali_.get_biopython_align_codon2aa(),
            )
    except Exception as e:
        print("somehting wrong when converting %s to %s, %s" % (input, phylip, str(e)))
        return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="argument", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "--input",
        type=str,
        required=True,
    )

    parser.add_argument(
        "--phylip",
        type=str,
        required=True,
    )

    args = parser.parse_args()
    codon2aa(input=args.input, phylip=args.phylip)
