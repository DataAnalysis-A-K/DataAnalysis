import requests
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = "https://publicreporting.cftc.gov/resource/6dca-aqww.json"

def find_contract_names():
    params = {
        "$select": "distinct contract_market_name",
        "$where": "contract_market_name like '%BITCOIN%'",
    }

    r = requests.get(BASE_URL, params=params, headers={"User-Agent": "python-requests"})

    r.raise_for_status()

    return [row["contract_market_name"] for row in r.json()]

def fetch_cot_data(contract_name, weeks=50):
    params = {
        "$where": f"contract_market_name like '{contract_name}'",
        "$order": "report_date_as_yyyy_mm_dd DESC",
        "$limit": weeks,
    }

    r = requests.get(BASE_URL, params=params, headers={"User-Agent": "python-requests"})

    r.raise_for_status()

    data = r.json()

    if not data:
        raise ValueError(f"Žiadne dáta pre '{contract_name}'. Skontroluj presný nazov cez find_contract_name().")

    df_inner = pd.DataFrame(data)

    df_inner["report_date_as_yyyy_mm_dd"] = pd.to_datetime(df_inner["report_date_as_yyyy_mm_dd"])

    numeric_cols = [
        "open_interest_all",
        "comm_positions_long_all",
        "comm_positions_short_all",
        "noncomm_positions_long_all",
        "noncomm_positions_short_all",
    ]

    for c in numeric_cols:
        if c in df_inner.columns:
            df_inner[c] = pd.to_numeric(df_inner[c], errors="coerce")

    df_inner = df_inner.sort_values("report_data_as_yyyy_mm_dd").reset_index(drop=True)

    dup_counts = df_inner.groupby("report_data_as_yyyy_mm_dd").size()

    if (dup_counts > 1).any():
        print("VAROVANIE: viacero riadkov pre rovnaký dátum - skontroluj filter!")
        print(dup_counts[dup_counts > 1])

    df_inner["comm_net"] = df_inner["comm_positions_long_all"] - df_inner["comm_positions_short_all"]
    df_inner["noncomm_net"] = df_inner["noncomm_positions_long_all"] - df_inner["noncomm_positions_short_all"]

    return df_inner

def plot_cot(df_inner, contract_name):
    fig, axes = plt.subplots(
        nrows=2, ncols=1, figsize=(12, 8), sharex=True
    )

    ax_1 = axes[0]

    # Commercials Long Positions
    ax_1.plot(
        df_inner["report_date_as_yyyy_mm_dd"], df_inner["comm_positions_long_all"], label="Commercials Long", color="green"
    )

    # Commercials Short Positions
    ax_1.plot(
        df_inner["report_date_as_yyyy_mm_dd"], df_inner["comm_positions_short_all"], label="Commercials Short", color="red"
    )

    # Non-Commercials Long Positions
    ax_1.plot(
        df_inner["report_date_as_yyyy_mm_dd"], df_inner["noncomm_positions_long_all"], label="Non-Commercials (Fondy) Long", color="blue", linestyle="--"
    )

    # Non-Commercials Short Positions
    ax_1.plot(
        df_inner["report_date_as_yyyy_mm_dd"], df_inner["noncomm_positions_short_all"], label="Non-Commercials (Fondy) Short", color="orange", linestyle="--"
    )

    ax_1.set_title(f"CFTC COT — {contract_name} — Long vs Short pozície", fontsize=14, fontweight="bold")
    ax_1.set_ylabel("Počet kontraktov")
    ax_1.legend()
    ax_1.grid(alpha=0.3)

    ax_2 = axes[1]

    # Commercials Net
    ax_2.bar(
        df_inner["report_date_as_yyyy_mm_dd"], df_inner["comm_net"], width=4, label="Commercials Net", color="green", alpha=0.6
    )

    # Non-Commercials Net
    ax_2.bar(
        df_inner["report_date_as_yyyy_mm_dd"], df_inner["noncomm_net"], width=4, label="Non-Commercials Net", color="blue", alpha=0.6
    )

    ax_2.axhline(0, color="black", linewidth=0.8)
    ax_2.set_title("Net pozície (Long − Short)", fontsize=14, fontweight="bold")
    ax_2.set_ylabel("Net kontrakty")
    ax_2.set_xlabel("Dátum reportu")
    ax_2.grid(alpha=0.3)

    plt.tight_layout()

    plt.savefig("outputs/cftc_bitcoin_cot.png")
    plt.show()

names = find_contract_names()

print("Dostupné kontrakty obsahujúce 'BITCOIN':")

for n in names:
    print(" -", n)

target = next((n for n in names if "MICRO" not in n.upper()), names[0])
print(f"\nPoužívam kontrakt: {target}\n")

df = fetch_cot_data(target)

print(df[["report_date_as_yyyy_mm_dd", "comm_net", "noncomm_net", "open_interest_all"]].tail(10))

plot_cot(df, target)