import pandas as pd
from datetime import date, timedelta

def calculate_end_date(df, row_index):
    next_row = df.iloc[row_index + 1] if row_index < len(df) - 1 else None
    if next_row is not None and next_row["Employee Code"] == df.loc[row_index, "Employee Code"]:
        return next_row["Effective Date"] - timedelta(days=1)
    else:
        return date(2100, 1, 1)

def handle_missing_data(df, col_name, row_index):
    previous_value = None
    for i in range(row_index - 1, -1, -1):
        if not pd.isna(df.loc[i, col_name]):
            previous_value = df.loc[i, col_name]
            break
    return previous_value if previous_value is not None else df.loc[row_index, col_name]

def transform_data(df):
    transformed_data = []
    for i in range(len(df)):
        row = df.iloc[i]
        employee_code = row["Employee Code"]
        manager_code = row["Manager Employee Code"]
        effective_date = pd.to_datetime(row["Date of Joining"])
        end_date = calculate_end_date(df, i)
        last_compensation = handle_missing_data(df, "Compensation", i)
        compensation = row["Compensation"]
        last_pay_raise_date = None if last_compensation == compensation else pd.to_datetime(row["Compensation 1 date"])
        variable_pay = pd.NA  # Assuming missing for this example
        # Option 1: Convert effective_date to date:
        tenure = (end_date - effective_date.date()).days
        # Option 2: Convert end_date to Timestamp:
        # tenure = (end_date - pd.to_datetime(effective_date)).days
        performance_rating = handle_missing_data(df, "Review 1", i)
        engagement_score = handle_missing_data(df, "Engagement 1", i)
        transformed_data.append({
            "Employee Code": employee_code,
            "Manager Employee Code": manager_code,
            "Last Compensation": last_compensation,
            "Compensation": compensation,
            "Last Pay Raise Date": last_pay_raise_date,
            "Variable Pay": variable_pay,
            "Tenure in Org": tenure,
            "Performance Rating": performance_rating,
            "Engagement Score": engagement_score,
            "Effective Date": effective_date,
            "End Date": end_date
        })
    return pd.DataFrame(transformed_data)

# Read input data
df = pd.read_csv("input.csv")

# Transform data
transformed_df = transform_data(df.copy())

# Sort and export data
transformed_df.sort_values(by=["Employee Code", "Effective Date"], inplace=True)
transformed_df.to_csv("result.csv", index=False)

print("Data transformation complete!")
