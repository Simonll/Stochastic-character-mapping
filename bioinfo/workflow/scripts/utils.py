from typing import List, Set
from typing import Union
from collections import defaultdict
from itertools import product
import numpy as np
import pandas as pd
from cogent3.util.union_dict import UnionDict

aa: List[str] = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]

sub: List[str] = [i + ">" + j for i, j in product(aa, aa) if i != j]


def get_set_of_keys() -> Set[str]:
    set_of_keys: Set[str] = set()
    for i in sub:
        a, b = i.split(">")
        k_: str = a + "<>" + b if a < b else b + "<>" + a
        if k_ not in set_of_keys:
            set_of_keys.add(k_)
    return set_of_keys
    
def prop(x):
    return np.sum(x) / x.shape[0]


def compute_entropy(df_profile: pd.DataFrame) -> float:

    return np.exp(
        -(df_profile * df_profile.apply(lambda x: np.log(x), axis=1)).sum(axis=1)
    )


AA_COLORS = {
    "GAVLI": "#009999",
    "FYW": "#ff6600",
    "CM": "orange",
    "ST": "#009900",
    "KRH": "#FF0102",
    "DE": "blue",
    "NQ": "#993300",
    "P": "#cc0099",
}

AA_COLORS_NIC = {
    "AGST": "#009999",  # Small nonpolar
    "FYW": "#ff6600",  # Aromatic
    "ILVM": "orange",  # Nonpolar aliphatic
    "HKR": "#009900",  # Polar positive
    "DE": "#FF0102",  # Polar negative
    "NQ": "blue",  # Polar neutral
    "P": "#993300",  # Proline
    "C": "#cc0099",  # Cysteine
}

AA_COLORS_SLL = {
    "AGST": "#1f77b4",  # Small nonpolar (blue)
    "FYW": "#ff7f0e",  # Aromatic (orange)
    "ILVM": "#2ca02c",  # Nonpolar aliphatic (green)
    "HKR": "#d62728",  # Polar positive (red)
    "DE": "#9467bd",  # Polar negative (purple)
    "NQ": "#17becf",  # Polar neutral (cyan)
    "P": "#8c564b",  # Proline (brown)
    "C": "#e377c2",  # Cysteine (pink)
}


class _DefaultValue:
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value


def expand_colors(base, colors):
    base = base.copy()
    base.update({ch: clr for chars, clr in colors.items() for ch in chars})
    return base


_gray = _DefaultValue("gray")

base_colors = defaultdict(_gray)


def get_base_logo_layout(axnum, xtick_fontsize, ytick_fontsize):
    """creates default plotly layout for drawing a sequence logo
    Parameters
    ----------
    axnum : int
        axis number for plotly
    xtick_fontsize, ytick_fontsize : int
        font size for tick values

    Returns
    -------
    UnionDict
    """
    layout = UnionDict()

    # set x and y range, set y ticks
    axis_lines = dict(
        mirror=True,
        linewidth=1,
        showgrid=False,
        linecolor="black",
        showline=False,
        visible=False,
        zeroline=False,
        ticks="",
    )
    axis = "axis" if axnum == 1 else f"axis{axnum}"
    xanchor = "x" if axnum == 1 else f"x{axnum}"
    yanchor = "y" if axnum == 1 else f"y{axnum}"

    layout[f"x{axis}"] = dict(
        anchor=yanchor,
        tickfont=dict(size=xtick_fontsize),
        ticks="inside",
        showticklabels=False,  # Disable x-axis tick labels
        domain=[0, 1],  # Use the full height of the plot for the y-axis
    )

    layout[f"y{axis}"] = dict(
        tickfont=dict(size=ytick_fontsize),
        title="",  # title="frequency",
        anchor=xanchor,
        ticks="inside",
        showticklabels=False,  # Disable y-axis tick labels
        domain=[0, 1],  # Use the full height of the plot for the y-axis
    )

    layout.margin = dict(
        l=0, r=0, t=0, b=0
    )  # Reduce top margin to bring the title closer

    layout.title = dict(
        text="Title Text",  # Adjust this as needed
        x=0.5,  # Center title horizontally
        y=0.98,  # Adjust vertical position to move it closer to the image
        xanchor="center",
        yanchor="top",
        font=dict(size=14),  # Set font size for the title
    )

    layout[f"x{axis}"] |= axis_lines
    layout[f"y{axis}"] |= axis_lines
    layout.template = "plotly_white"
    return layout


def _char_hts_as_lists(data):
    """returns a [[(base, height), ..], ..]"""
    # data is assumed row-oriented
    result = []
    for d in data:
        try:
            d = d.to_dict()
        except AttributeError:
            # assume it's just a dict
            pass

        if d:
            d = list(d.items())
        else:
            d = None
        result.append(d)

    return result


def add_header(input, header, output):

    # Open the file in write mode and write the header
    with open(output, "w") as f:
        f.write(header + "\n")  # Write the header and a newline

    # Open the file in append mode and append the data from the original CSV
    with open(output, "a") as f:
        with open(input, "r") as original:
            f.write(original.read())  # Append all data from the original CSV
