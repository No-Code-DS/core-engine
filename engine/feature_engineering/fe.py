import pandas as pd

from engine.feature_engineering.schema import FeRequest


def magic_fe(data: pd.DataFrame, fe_config: FeRequest) -> pd.DataFrame:
    operation = fe_config.operation_symbol
    if operation == "+":
        data[fe_config.name] = data[fe_config.left] + data[fe_config.right]
    elif operation == "-":
        data[fe_config.name] = data[fe_config.left] - data[fe_config.right]
    elif operation == "*":
        data[fe_config.name] = data[fe_config.left] * data[fe_config.right]
    elif operation == "/":
        data[fe_config.name] = data[fe_config.left] / data[fe_config.right]
    return data
