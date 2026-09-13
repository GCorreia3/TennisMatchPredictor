from playwright.sync_api import sync_playwright
import pandas as pd
from io import StringIO

# current week url
start_url = (
    "https://www.atptour.com/en/rankings/singles"
    "?rankRange=1-2000"
    "&region=all"
)

def get_url(date):
    date_string = f"{date}"
    date_string = date_string[:4] + "-" + date_string[4:6] + "-" + date_string[6:]
    return f"https://www.atptour.com/en/rankings/singles?dateWeek={date_string}&rankRange=1-2000&region=all"

def create_dataframe(table_html, date):
    df = pd.read_html(StringIO(table_html))[0]
    df = df.drop(10) # remove empty row
    df["ranking_date"] = date
    df = df[
        [
            "ranking_date",
            "Hidden header",
            "Player",
            "Official Points"
        ]
    ].copy()
    df = df.rename(columns={
        "Hidden header": "rank",
        "Player": "player",
        "Official Points": "ranking_points"
    })
    df["rank"] = range(1, len(df) + 1)
    df["player"] = df["player"].str.replace(r"^[+-]?\d+\s*", "", regex=True).str.strip()

    return df

def get_table_html(url):
    page.goto(url, wait_until="domcontentloaded")
    page.locator("table").nth(1).locator("tbody tr").first.wait_for()

    table_html = page.locator("table").nth(1).evaluate(
        "(table) => table.outerHTML"
    )

    return table_html

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    table_html = get_table_html(start_url)

    # Get list of dates from website
    date_list = []

    date_select = page.locator("select").nth(2)
    dates = date_select.locator("option")

    for i in range(dates.count()):
        date_i = dates.nth(i).inner_text()
        date_i = date_i.replace(".", "")
        int_date = int(date_i)
        if int_date < 20200000:
            break
        if int_date < 20210000:
            date_list.append(date_i)

    context.close()

    df_list = []

    for i, date in enumerate(date_list):
        # if i == 0: # first date
        #     df = create_dataframe(table_html, date)
        #     df_list.append(df)
        #     print(i)
        #     browser.close()
        # else:

        # browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        url = get_url(date)
        table_html = get_table_html(url)
        df = create_dataframe(table_html, date)
        df_list.append(df)
        print(i)
        context.close()

    browser.close()

df_matches = pd.concat(df_list, axis=0, ignore_index=True)

df_matches.to_csv(
    "atp_rankings_2020.csv",
    index=False
)
