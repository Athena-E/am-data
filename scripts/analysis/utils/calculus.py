

def differentiate(df, u, v, new_name):
    """
    Computes the numerical derivative of column `u` with respect to column `v` in a DataFrame.

    The derivative is calculated as the difference of consecutive values in `u` divided by 
    the difference of consecutive values in `v`. The result is stored in a new column specified 
    by `new_name`.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        u (str): The name of the column to differentiate.
        v (str): The name of the column with respect to which the differentiation is performed.
        new_name (str): The name of the new column to store the result of the differentiation.

    Raises:
        AssertionError: If `u` or `v` are not present in the DataFrame columns.
    """
    assert u in df.columns, f"DataFrame must include {u}"
    assert v in df.columns, f"DataFrame must include {v}"
    df.loc[0:len(df), [new_name]] = 0.0

    for i in range(1, len(df)):
        du = df[u].iloc[i] - df[u].iloc[i - 1]
        dv = df[v].iloc[i] - df[v].iloc[i - 1]

        if dv != 0:
            df.at[i, new_name] = du / dv

def integrate(df, u, v, new_name):
    """
    Computes the numerical integral of column `u` with respect to column `v` in a DataFrame.

    The integral is approximated using the trapezoidal rule, where the average of consecutive 
    values of `u` is multiplied by the change in `v` to estimate the integral at each point.

    Args:
        df (pd.DataFrame): The DataFrame containing the data.
        u (str): The name of the column to integrate.
        v (str): The name of the column with respect to which the integration is performed.
        new_name (str): The name of the new column to store the result of the integration.

    Raises:
        AssertionError: If `u` or `v` are not present in the DataFrame columns.
    """
    assert u in df.columns, f"DataFrame must include {u}"
    assert v in df.columns, f"DataFrame must include {v}"
    df.loc[0:len(df), [new_name]] = 0.0

    for i in range(1, len(df)):
        avg_u = (df[u].iloc[i] + df[u].iloc[i - 1]) / 2
        dv = df[v].iloc[i] - df[v].iloc[i - 1]
        
        df.at[i, new_name] = df[new_name].iloc[i - 1] + avg_u * dv
