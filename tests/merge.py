import pandas as pd
from tests.extract_load import Extractors


def merge_data(account_data: dict) -> pd.DataFrame:
    """Uses the provided dict with account names and path to the extracts. \n
    Adds the account name to each entry. \n
    Concatenates all dfs and handles the empty value dates by copying the date of the transaction.

    Args:
        account_data (dict): Dictionary with account names as keys and path of file as values
    Returns:
        pd.DataFrame: Concatenated result of account dataframes
    """
    dataframes = []
    for account, path in account_data.items():
        if path != None:
            df = Extractors.accounts[account](path)

            if 'balance' in df.columns:
                cols = list(df.columns)
                idx = cols.index('balance')
                cols[idx] = 'account_balance'
                df.columns = cols
            df['account'] = account
            df['account_balance'] = df['account_balance'].astype(float)

            dataframes.append(df)

    main = pd.concat(dataframes)
    main.reset_index(drop=True, inplace=True)

    # Handle empty value date
    for index, row in main.iterrows():
        if pd.isna(row.value_date):
            main.at[index, 'value_date'] = main.loc[index].date

    main.sort_values('date', ascending=False, inplace=True)
    main.reset_index(drop=True, inplace=True)

    return main
