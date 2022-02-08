import os
import requests
import urllib.parse
import json
import re

from flask import redirect, render_template, request, session
from functools import wraps

url = 'https://graphql.anilist.co'

regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def check(email):
    if(re.search(regex, email)):
        return True

    else:
        return False

def manga_name(name):
    query = '''
    query ($search: String, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: MANGA, search: $search) {
                id
                coverImage {
                    large
                }
                title {
                    romaji
                    english
                }
                isAdult
            }
        }
    }
    '''
    variables = {
        'search': name,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    media = response2["data"]["Page"]["media"]
    total = response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        loss = { 'total': total }
        return loss

    coverImage, title_english, title_romaji, adult = ([] for z in range(4))

    # print(len(media))

    for i in range(len(media)):
        coverImage.append(media[i]["coverImage"]["large"])
        title_english.append(media[i]["title"]["english"])
        title_romaji.append(media[i]["title"]["romaji"])
        adult.append(media[i]["isAdult"])

    information = {
        "total": total,
        "coverImage": coverImage,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "adult" : adult
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)

def anime_name(name):
    query = '''
    query ($search: String, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: ANIME, search: $search) {
                id
                coverImage {
                    large
                }
                title {
                    romaji
                    english
                }
                isAdult
            }
        }
    }
    '''
    variables = {
        'search': name,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    media = response2["data"]["Page"]["media"]
    total = response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        loss = { 'total': total }
        return loss

    coverImage, title_english, title_romaji, adult = ([] for z in range(4))

    # print(len(media))

    for i in range(len(media)):
        coverImage.append(media[i]["coverImage"]["large"])
        title_english.append(media[i]["title"]["english"])
        title_romaji.append(media[i]["title"]["romaji"])
        adult.append(media[i]["isAdult"])

    information = {
        "total": total,
        "coverImage": coverImage,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "adult" : adult
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)

def manga(score):
    query = '''
    query ($score: Int, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: MANGA, averageScore_greater: $score) {
                id
                coverImage {
                    large
                }
                title {
                    romaji
                    english
                }
                isAdult
            }
        }
    }
    '''
    variables = {
        'score': score,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    media = response2["data"]["Page"]["media"]
    total = response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        return

    coverImage, title_english, title_romaji, adult = ([] for z in range(4))

    # print(len(media))

    for i in range(len(media)):
        coverImage.append(media[i]["coverImage"]["large"])
        title_english.append(media[i]["title"]["english"])
        title_romaji.append(media[i]["title"]["romaji"])
        adult.append(media[i]["isAdult"])

    information = {
        "total": total,
        "coverImage": coverImage,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "adult" : adult
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)

def manga_genre(score, genre):
    query = '''
    query ($score: Int, $page: Int, $perPage: Int, $genre: [String]) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: MANGA, genre_in: $genre, averageScore_greater: $score) {
                id
                coverImage {
                    large
                }
                title {
                    romaji
                    english
                }
                isAdult
            }
        }
    }
    '''
    variables = {
        'score': score,
        'genre': genre,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    # print(response2)

    media = response2["data"]["Page"]["media"]
    total = response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        return

    coverImage, title_english, title_romaji, adult = ([] for z in range(4))

    # print(len(media))

    for i in range(len(media)):
        coverImage.append(media[i]["coverImage"]["large"])
        title_english.append(media[i]["title"]["english"])
        title_romaji.append(media[i]["title"]["romaji"])
        adult.append(media[i]["isAdult"])

    information = {
        "total": total,
        "coverImage": coverImage,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "adult" : adult
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)

def anime_genre(score, genre):
    query = '''
    query ($score: Int, $page: Int, $perPage: Int, $genre: [String]) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: ANIME, genre_in: $genre, averageScore_greater: $score) {
                id
                coverImage {
                    large
                }
                title {
                    romaji
                    english
                }
                isAdult
            }
        }
    }
    '''
    variables = {
        'score': score,
        'genre': genre,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    # print(response2)

    media = response2["data"]["Page"]["media"]
    total = response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        return

    coverImage, title_english, title_romaji, adult = ([] for z in range(4))

    # print(len(media))

    for i in range(len(media)):
        coverImage.append(media[i]["coverImage"]["large"])
        title_english.append(media[i]["title"]["english"])
        title_romaji.append(media[i]["title"]["romaji"])
        adult.append(media[i]["isAdult"])

    information = {
        "total": total,
        "coverImage": coverImage,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "adult" : adult
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)

def anime(score):
    query = '''
    query ($score: Int, $page: Int, $perPage: Int) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: ANIME, averageScore_greater: $score) {
                id
                coverImage {
                    large
                }
                title {
                    romaji
                    english
                }
                isAdult
            }
        }
    }
    '''
    variables = {
        'score': score,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    media = response2["data"]["Page"]["media"]
    total = response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        return

    coverImage, title_english, title_romaji, adult = ([] for z in range(4))

    # print(len(media))

    for i in range(len(media)):
        coverImage.append(media[i]["coverImage"]["large"])
        title_english.append(media[i]["title"]["english"])
        title_romaji.append(media[i]["title"]["romaji"])
        adult.append(media[i]["isAdult"])

    information = {
        "total": total,
        "coverImage": coverImage,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "adult" : adult
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)

def search_manga_name(name):
    query = '''
    query ($page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: MANGA, search: $search) {
                id
                coverImage {
                    large
                }
                bannerImage
                description
                averageScore
                status
                title {
                    romaji
                    english
                    native
                }
                isAdult
                season
                chapters
                volumes
                popularity
                genres
                characters (page: 1, perPage: 25) {
                    edges {
                        role
                        node {
                            id
                            name{
                                full
                            }
                            image {
                                large
                            }
                            gender
                            age
                        }
                    }
                }
                reviews (page: 1, perPage: 25) {
                    edges {
                        node {
                            id
                            summary
                            rating
                        }
                    }
                }
            }
        }
    }
    '''
    variables = {
        'search': name,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})

    response2 = response.json()

    media = response2["data"]["Page"]["media"]
    total= response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        return

    rating = ""
    summary = ""

    age, gender, name, image, role = ([] for t in range(5))

    for i in range(len(media)):
        characters = media[i]["characters"]["edges"]
        reviews = media[i]["reviews"]["edges"]
        season = media[i]["season"]

        for y in range(len(characters)):
            age.append(characters[y]["node"]["age"])
            gender.append(characters[y]["node"]["gender"])
            image.append(characters[y]["node"]["image"]["large"])
            name.append(characters[y]["node"]["name"]["full"])
            role.append(characters[y]["role"])

        for z in range(len(reviews)):
            rating = reviews[z]["node"]["rating"]
            summary = reviews[z]["node"]["summary"]

        isAdult = media[i]["isAdult"]
        description = media[i]["description"]
        genres = media[i]["genres"]
        title_english = media[i]["title"]["english"]
        native = media[i]["title"]["native"]
        title_romaji = media[i]["title"]["romaji"]
        chapter = media[i]["chapters"]
        volume = media[i]["volumes"]
        coverImage = media[i]["coverImage"]["large"]
        bannerImage = media[i]["bannerImage"]
        description = media[i]["description"]
        popular = media[i]["popularity"]
        status =  media[i]["status"]
        average = media[i]["averageScore"]

    print(native)

    information = {
        "native": native,
        "name": name,
        "age": age,
        "gender": gender,
        "image": image,
        "rating": rating,
        "role": role,
        "summary": summary,
        "coverImage": coverImage,
        "bannerImage": bannerImage,
        "description": description,
        "genres": genres,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "chapter": chapter,
        "volume": volume,
        "adult": isAdult,
        "total": total,
        "season": season,
        "popular": popular,
        "status": status,
        "average": average
    }

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)


def search_anime_name(name):
    query = '''
    query ($page: Int, $perPage: Int, $search: String) {
        Page (page: $page, perPage: $perPage) {
            pageInfo {
                total
                currentPage
                lastPage
                hasNextPage
                perPage
            }
            media (type: ANIME, search: $search) {
                id
                coverImage {
                    large
                }
                bannerImage
                description
                averageScore
                status
                title {
                    romaji
                    english
                    native
                }
                isAdult
                season
                episodes
                duration
                popularity
                genres
                characters (page: 1, perPage: 25) {
                    edges {
                        role
                        node {
                            id
                            name{
                                full
                            }
                            image {
                                large
                            }
                            gender
                            age
                        }
                    }
                }
                reviews (page: 1, perPage: 25) {
                    edges {
                        node {
                            id
                            summary
                            rating
                        }
                    }
                }
            }
        }
    }
    '''
    # print(name)
    variables = {
        'search': name,
        'page': 1,
        'perPage': 50
    }

    response = requests.post(url, json={'query': query, 'variables': variables})
    # print(response)

    if not response:
        return

    response2 = response.json()
    # print(response2)

    rating = ""
    summary = ""

    media = response2["data"]["Page"]["media"]
    total= response2["data"]["Page"]["pageInfo"]["total"]

    if total == 0:
        return

    age, gender, name, image, role = ([] for t in range(5))

    for i in range(len(media)):
        characters = media[i]["characters"]["edges"]
        reviews = media[i]["reviews"]["edges"]
        season = media[i]["season"]

        for y in range(len(characters)):
            age.append(characters[y]["node"]["age"])
            gender.append(characters[y]["node"]["gender"])
            image.append(characters[y]["node"]["image"]["large"])
            name.append(characters[y]["node"]["name"]["full"])
            role.append(characters[y]["role"])

        for z in range(len(reviews)):
            rating = reviews[z]["node"]["rating"]
            summary = reviews[z]["node"]["summary"]

        isAdult = media[i]["isAdult"]
        genres = media[i]["genres"]
        title_english = media[i]["title"]["english"]
        native = media[i]["title"]["native"]
        title_romaji = media[i]["title"]["romaji"]
        episode = media[i]["episodes"]
        duration = media[i]["duration"]
        coverImage = media[i]["coverImage"]["large"]
        bannerImage = media[i]["bannerImage"]
        description = media[i]["description"]
        popular = media[i]["popularity"]
        status =  media[i]["status"]
        average = media[i]["averageScore"]

    # print("extracting complete")
    # print(name)

    information = {
        "native": native,
        "name": name,
        "age": age,
        "gender": gender,
        "image": image,
        "rating": rating,
        "role": role,
        "summary": summary,
        "coverImage": coverImage,
        "bannerImage": bannerImage,
        "description": description,
        "genres": genres,
        "Etitle": title_english,
        "Rtitle": title_romaji,
        "episode": episode,
        "duration": duration,
        "adult": isAdult,
        "total": total,
        "season": season,
        "popular": popular,
        "status": status,
        "average": average
    }
    # print("returning")

    #clear everything in list and dict

    return (information)

    if information:
        information = information.fromkeys(information, 0)

    if media:
        media = media.fromkeys(media, 0)

    if total:
        total = total.fromkeys(total, 0)