from bs4 import BeautifulSoup as Soup
from bs4 import Comment as BSComment
import requests as req
import pandas as pd

def scrape_data(page_url, div_id, index):
    print(f"Fetching data from: {page_url}, Div ID: {div_id}")
    response = req.get(page_url)
    page_content = Soup(response.content, 'html.parser')
    target_div = page_content.find('div', {'id': div_id})
    
    if target_div is None:
        print(f"Error: Could not locate the div with ID '{div_id}' on {page_url}")
        return

    comments = target_div.find_all(string=lambda text: isinstance(text, BSComment))
    if not comments:
        print(f"Error: No comments found in the div with ID '{div_id}' on {page_url}")
        return

    rows = Soup(comments[0], 'html.parser').find_all('tr')
    collected_data = {}

    # Initialize the dictionary for storing player data
    for idx, header in enumerate(rows[1].find_all('th')):
        if idx != 0:
            collected_data[header.get('data-stat')] = []

    for row in rows[2:]:
        player_info = row.find_all('td')
        for data_cell in player_info:
            stat_type = data_cell.get('data-stat')
            if stat_type in collected_data:
                if stat_type == 'nationality':
                    nationality_parts = data_cell.getText().split(" ")
                    collected_data[stat_type].append(nationality_parts[0])
                else:
                    collected_data[stat_type].append(data_cell.getText())

    player_dataframe = pd.DataFrame(collected_data)

    # Remove specific columns for goalkeepers if needed
    if index == 2:
        player_dataframe.drop(['gk_games', 'gk_games_starts', 'gk_minutes', 'minutes_90s'], axis=1, inplace=True)

    player_dataframe.to_csv(f'table{index}.csv')

def consolidate_data():
    try:
        base_data = pd.read_csv('table1.csv')
    except FileNotFoundError:
        print("Error: Unable to locate table1.csv. Please ensure it exists.")
        return

    for i in range(3, 11):
        new_table = pd.read_csv(f"table{i}.csv")
        for column in new_table.columns:
            if column in base_data.columns and column != 'Unnamed: 0':
                new_table.drop(column, axis=1, inplace=True)
        base_data = pd.merge(base_data, new_table, on=['Unnamed: 0'], how='inner')

    # Merge with the second table based on common columns
    common_columns = [col for col in pd.read_csv("table2.csv").columns if col in base_data.columns]
    common_columns.pop(0)  # Remove the first column for merging
    final_data = pd.merge(base_data, pd.read_csv("table2.csv"), on=common_columns, how='left')

    # Cleanup unnecessary columns and convert minutes
    final_data.drop(['Unnamed: 0_x', 'Unnamed: 0_y', 'minutes_90s', 'birth_year', 'matches'], axis=1, inplace=True)
    final_data['minutes'] = final_data['minutes'].apply(lambda x: int(''.join(x.split(','))))
    
    # Filter and sort data
    filtered_data = final_data[final_data['minutes'] > 90]
    sorted_data = filtered_data.sort_values(by=["player", 'age'], ascending=[True, False])
    sorted_data.to_csv('result.csv')

if __name__ == '__main__':
    main_url = 'https://fbref.com/en/comps/9/2023-2024/stats/2023-2024-Premier-League-Stats'
    main_response = req.get(main_url)
    main_soup = Soup(main_response.content, 'html.parser')
    main_table = main_soup.find('div', {'id': 'all_stats_standard'})

    if main_table is None:
        print("Error: Could not find the main stats table.")
    else:
        main_comments = main_table.find_all(string=lambda text: isinstance(text, BSComment))
        
        if main_comments:
            main_data = Soup(main_comments[0], 'html.parser').find_all('tr')
            if len(main_data) > 1:
                excluded_indices = [0, 6, 10, 11, 13, 16, 22, 36]
                main_stats = {}

                for idx, header in enumerate(main_data[1].find_all('th')):
                    if idx not in excluded_indices:
                        main_stats[header.get('data-stat')] = []

                for row in main_data[2:]:
                    player_data = row.find_all('td')
                    for data_cell in player_data:
                        if data_cell.get('data-stat') in main_stats:
                            if data_cell.get('data-stat') == 'nationality':
                                nationality_parts = data_cell.getText().split(" ")
                                main_stats[data_cell.get('data-stat')].append(nationality_parts[0])
                            else:
                                main_stats[data_cell.get('data-stat')].append(data_cell.getText())

                main_dataframe = pd.DataFrame(main_stats)
                main_dataframe.rename(columns={'goals_pens': 'Non-Penalty Goals', 'pens_made': 'Penalty Goals'}, inplace=True)
                main_dataframe.to_csv('table1.csv')
            else:
                print("Error: Expected format does not contain sufficient data.")
        else:
            print("Error: No comments detected within the table.")

    urls_to_scrape = [
        'https://fbref.com/en/comps/9/2023-2024/keepers/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/shooting/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/passing/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/passing_types/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/gca/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/defense/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/possession/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/playingtime/2023-2024-Premier-League-Stats',
        'https://fbref.com/en/comps/9/2023-2024/misc/2023-2024-Premier-League-Stats'
    ]
    
    div_ids = [
        'all_stats_keeper', 'all_stats_shooting', 'all_stats_passing',
        'all_stats_passing_types', 'all_stats_gca', 'all_stats_defense',
        'all_stats_possession', 'all_stats_playing_time', 'all_stats_misc'
    ]
    
    for index, (url, div_id) in enumerate(zip(urls_to_scrape, div_ids)):
        scrape_data(url, div_id, index + 2)
    
    consolidate_data()
