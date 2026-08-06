"""
visualize.py
==========
Responsible for ONE thing: taking the cleaned fact table from clean.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def visualize_customer_tiers(df: pd.DataFrame) -> None:
    """
    Visualize the distribution of customers across spend tiers.
    """
    df["PctOfCustomers"] = (
    df["CustomerCount"] / df["CustomerCount"].sum() * 100
    )
    plot_df = (
        df.rename(columns={
            "PctOfCustomers": "Customers",
            "PctOfRevenue": "Revenue"
        })
        .melt(
            id_vars="CustomerTier",
            value_vars=["Customers", "Revenue"],
            var_name="Metric",
            value_name="Percentage"
        )
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=plot_df,
        x="CustomerTier",
        y="Percentage",
        hue="Metric",
        palette="viridis",
        ax=ax
    )
    ax.set_title("Customer and Revenue Distribution by Spend Tier")
    ax.set_xlabel("Customer Spend Tier")
    ax.set_ylabel("Percentage (%)")
    ax.set_ylim(0, 60)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return fig

def visualize_monthly_growth(df: pd.DataFrame) -> None:
    """
    Visualize the monthly revenue growth.
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x="Month",
        y="MonthlyRevenue",
        data=df,
        color="skyblue",
        ax=ax1,
        label="Revenue"
    )
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Revenue ($)")
    ax1.tick_params(axis="y")
    
    ax2 = ax1.twinx()
    sns.lineplot(
        x="Month",
        y="MonthlyGrowthPct",
        data=df,
        marker="o",
        color="red",
        ax=ax2,
        label="Growth Rate"
    )
    ax2.set_ylabel("Growth Rate (%)")
    ax1.tick_params(axis='x', rotation=90)
    ax2.legend_.remove()
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(
        lines + lines2,
        labels + labels2,
        loc='upper left'
    )
    plt.title("Monthly Revenue and Growth Rate")
    plt.tight_layout()
    plt.show()

    return fig

def visualize_purchase_cadence(df: pd.DataFrame) -> None:
    """
    Visualize the distribution of purchase cadence.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=df,
        x='PurchaseCadence',
        y='CustomerCount',
        hue='PurchaseCadence',
        palette='viridis',
        legend=False,
        ax=ax
    )

    for container in ax.containers:
        ax.bar_label(container, fmt='%d')

    ax.set_title('Customer Distribution by Purchase Cadence')
    ax.set_xlabel('Purchase Cadence')
    ax.set_ylabel('Number of Customers')
    plt.tight_layout()
    plt.show()

    return fig

def visualize_revenue_pareto(df: pd.DataFrame) -> None:
    """
    Visualize the revenue Pareto curve.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(x='CumulativePctCustomers', y='CumulativeRevenuePct', data=df, marker='o', color='green', ax=ax, label='Actual Cumulative Revenue')
    ax.axhline(80, color='red', linestyle='--', label='80% Revenue Threshold')
    perfect_line = [0, 100]
    ax.plot(perfect_line, perfect_line, color='gray', linestyle=':', label='Perfect Distribution')
    ax.legend()
    plt.title('Revenue Pareto Curve')
    plt.xlabel('Cumulative Percentage of Customers')
    plt.ylabel('Cumulative Percentage of Revenue')
    plt.tight_layout()
    plt.show()

    return fig