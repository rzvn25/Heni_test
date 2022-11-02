import pandas as pd
import re


def in_to_cm(*args):
    if None in list(args):
        return "NaN"
    result = 1
    for arg in list(args):
        result *= arg
    return result


def float_from_str(*args):
    if None in list(args) or '' in list(args):
        return "NaN"
    return float(args[0])


dim_df = pd.read_csv("candidateEvalData/dim_df_correct.csv")
print(dim_df)

regex_height = r"([\d\.]+)[\sx×]+[\d\.]+(?:[\D]+[\d\.]+)?\s?cm|(\d)\sby\s\d"
regex_width = r"[\d\.]+[\sx×]+([\d\.]+)(?:[\D]+[\d\.]+)?\s?cm|\d\sby\s(\d)"
regex_depth = r"[\d\.]+[\sx×]+[\d\.]+[\D]+([\d\.]+)?\s?cm"

heights = []
widths = []
depths = []
i = 0
for row in dim_df['rawDim']:
    cleaned_text = dim_df['rawDim'][i].replace(',', '.')
    height_matches = re.findall(regex_height, cleaned_text)
    if len(height_matches):
        height = height_matches[0]
        heights.append(float_from_str(height[0]) or in_to_cm(2.54 * height[1]))
    else:
        depths.append('NaN')

    width_matches = re.findall(regex_width, cleaned_text)
    if len(width_matches):
        width = width_matches[0]
        widths.append(float_from_str(width[0]) or in_to_cm(2.54 * width[1]))
    else:
        depths.append('NaN')

    depth_matches = re.findall(regex_depth, cleaned_text)
    if len(depth_matches) and '' not in depth_matches:
        depth = depth_matches[0]
        depths.append(float_from_str(depth[0]))
    else:
        depths.append('NaN')

    i = i + 1

print("heights")
print(heights)
print("widths")
print(widths)
print("depths")
print(depths)
