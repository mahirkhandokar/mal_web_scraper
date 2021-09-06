from bs4 import BeautifulSoup
import requests, os


def main():
    path = os.listdir('/Users/mahirkhandokar/Desktop/Projects/mal_web_scraper/anime')

    for file in path:
        del_path = os.path.join('/Users/mahirkhandokar/Desktop/Projects/mal_web_scraper/anime', file)
        os.remove(del_path)
    season = input('Please enter a season (e.g., Later, Winter 2022, etc.):')

    if season.title() == 'Later':
        html_text = requests.get('https://myanimelist.net/anime/season/later').text
    elif season.title() == 'Summer 2021':
        html_text = requests.get('https://myanimelist.net/anime/season').text
    elif (season[:-5].title() == 'Spring' or season[:-5].title() == 'Summer' or season[:-5].title() == 'Fall' or season[:-5].title() == 'Winter') and (int(season[-4:]) in  range(1917, 2023)) and (season.title() != 'Summer 2021' or season.title() != 'Later'):
        saison = season[:-5].lower()
        year = season[-4:]
        url = f'https://myanimelist.net/anime/season/{year}/{saison}'
        html_text = requests.get(url).text
    else:
        print('Enter an actual season found on MAL for example Fall 2021.')
        exit()

    soup = BeautifulSoup(html_text, 'lxml')
    animes = soup.find_all('div', class_='seasonal-anime js-seasonal-anime')
    
    answer = input('Do you want to specify the production studio? (Yes/No)').strip()
    if answer.title() == 'Yes':
        studio_input = input('Please enter the studio you prefer to have produced the anime (e.g., Kyoto Animation, Shaft, etc.):').strip()
    elif answer.title() == 'No':
        studio_input = ''
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    answer = input('Do you want to specify the number of episodes? (Yes/No)').strip()
    if answer.title() == 'Yes':
        episodes_input = input('Please enter the number of episodes you prefer the anime to have (e.g., 1, 12, etc.):').strip() + ' ep'
        if episodes_input != '1':
            episodes_input += 's'
    elif answer.title() == 'No':
        episodes_input = ''
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    answer = input('Do you want to specify the type of source material? (Yes/No)').strip()
    if answer.title() == 'Yes':
        source_mat_input = input('Please enter the type of source material you want the show to have (e.g., Manga, Light Novel, etc.):').title().strip()
    elif answer.title() == 'No':
        source_mat_input = ''
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    answer = input('Do you want to specify the genre(s)? (Yes/No)').strip()
    if answer.title() == 'Yes':
        genres_input = input('Please enter the genre(s) you want the anime to have as a comma separated list (e.g., Slice of Life, Comedy, etc.):').title()
        genres_input = genres_input.split(',')
        for i in range(len(genres_input)):
            genres_input[i] = genres_input[i].strip()
    elif answer.title() == 'No':
        genres_input = []
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    answer = input('Do you want to specify the anime format? (Yes/No)').strip()
    if answer.title() == 'Yes':
        anime_format_input = input('Please enter the type of anime you are looking for (e.g., TV, Special, etc.):').strip()
    elif answer.title() == 'No':
        anime_format_input = ''
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    answer = input('Do you want to specify the score range? (Yes/No)').strip()
    if answer.title() == 'Yes':
        score_input = input('Please enter the score range you prefer the anime to have (e.g., 9, 8, etc.):').strip() + '.'
    elif answer.title() == 'No':
        score_input = ''
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    answer = input('Do you want to specify the minimum number of members? (Yes/No)').strip()
    if answer.title() == 'Yes':
        members_input = input('Please enter the minimum number of members you prefer the anime to have (e.g., 100000, 200000, etc.):').strip()
    elif answer.title() == 'No':
        members_input = ''
    else:
        print('Not a valid answer, please enter Yes or No')
        exit()
    
    for index, anime in enumerate(animes):
        studio = anime.find('span', class_='producer')
        title = anime.find('a', class_='link-title')
        episodes = anime.find('div', class_='eps').a.span
        source_mat = anime.find('span', class_='source')
        genres = anime.find_all('span', class_='genre')
        info = anime.find('div', class_='info').text.split('-')
        anime_format = info[0].strip()
        release_date = info[1].strip()
        score_values = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'na']
        score = None
        i = 0
        while score == None:
            score = anime.find('span', class_ = f'score score-label score-{score_values[i]}')
            i += 1
        members = anime.find('span', class_='member fl-r')
        more_info = anime.h2.a['href']

        genres_count = 0

        if studio_input in studio.text:
            if episodes_input == episodes.text or episodes_input == '':
                if source_mat_input == source_mat.text or source_mat_input == '':
                    for i in genres_input:
                        for j in genres:
                            if i == j.text.strip():
                                genres_count += 1
                    if genres_count == len(genres_input):
                        if anime_format_input == anime_format or anime_format_input == '':
                            if score_input in score.text.strip():
                                if members_input == '' or int(members_input.replace(',', '')) <= int(members.text.replace(',', '').strip()) :
                                    with open(f'anime/{index + 1}.txt', 'w') as f:
                                        f.write(f'Title: {title.text} \n')
                                        f.write(f'Studio: {studio.text} \n')
                                        f.write(f'Number of Episodes: {episodes.text} \n')
                                        f.write(f'Source Material Type: {source_mat.text} \n')
                                        f.write('Genres: \n')
                                        for genre in genres:
                                            f.write(f'  {genre.text.strip()} \n')
                                        f.write(f'Anime Format: {anime_format} \n')
                                        f.write(f'Release Date: {release_date} \n')
                                        f.write(f'Score: {score.text.strip()} \n') 
                                        f.write(f'Number of Members: {members.text.strip()} \n')
                                        f.write(f'For more info visit: \n {more_info} \n')

                                        print(f'File Saved: {index + 1}')


if __name__ == '__main__':
    main()