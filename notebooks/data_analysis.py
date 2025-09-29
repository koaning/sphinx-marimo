import marimo

__generated_with = "0.1.0"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import pandas as pd
    import numpy as np
    return mo, np, pd


@app.cell
def __(mo):
    mo.md("# Data Analysis Example")
    return


@app.cell
def __(np, pd):
    # Generate sample data
    np.random.seed(42)
    df = pd.DataFrame({
        'Date': pd.date_range('2024-01-01', periods=100),
        'Sales': np.random.randint(50, 200, 100),
        'Customers': np.random.randint(10, 50, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
    })
    df['Revenue'] = df['Sales'] * np.random.uniform(10, 20, 100)
    return df,


@app.cell
def __(df, mo):
    mo.md(f"## Dataset Overview\n\nTotal records: **{len(df)}**")
    return


@app.cell
def __(df):
    df.head(10)
    return


@app.cell
def __(df, mo):
    region_select = mo.ui.dropdown(
        options=['All'] + list(df['Region'].unique()),
        value='All',
        label='Filter by Region'
    )
    region_select
    return region_select,


@app.cell
def __(df, region_select):
    filtered_df = (
        df if region_select.value == 'All'
        else df[df['Region'] == region_select.value]
    )
    return filtered_df,


@app.cell
def __(filtered_df, mo):
    stats = filtered_df.describe()
    mo.md(f"""
    ## Statistics for {region_select.value} Region

    - Average Sales: **{filtered_df['Sales'].mean():.2f}**
    - Total Revenue: **${filtered_df['Revenue'].sum():,.2f}**
    - Average Customers: **{filtered_df['Customers'].mean():.1f}**
    """)
    return stats,


@app.cell
def __(filtered_df, plt):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Sales over time
    axes[0].plot(filtered_df['Date'], filtered_df['Sales'].rolling(7).mean())
    axes[0].set_title('7-Day Moving Average of Sales')
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Sales')
    axes[0].grid(True, alpha=0.3)

    # Revenue by Region
    if region_select.value == 'All':
        region_revenue = df.groupby('Region')['Revenue'].sum()
        axes[1].bar(region_revenue.index, region_revenue.values)
        axes[1].set_title('Total Revenue by Region')
    else:
        axes[1].hist(filtered_df['Revenue'], bins=20)
        axes[1].set_title(f'Revenue Distribution - {region_select.value}')

    axes[1].set_xlabel('Region' if region_select.value == 'All' else 'Revenue')
    axes[1].set_ylabel('Total Revenue' if region_select.value == 'All' else 'Frequency')
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()
    fig
    return axes, fig


@app.cell
def __(mo):
    mo.md("""
    ---

    This notebook demonstrates data analysis capabilities with:
    - Pandas DataFrames
    - Interactive filtering
    - Dynamic visualizations
    - Statistical summaries
    """)
    return


if __name__ == "__main__":
    app.run()