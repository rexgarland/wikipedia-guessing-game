from lxml import html
import requests
import random

url = "https://en.wikipedia.org/wiki/Special:Random"

def get_sentence():
    page = requests.get(url)
    tree = html.fromstring(page.content)
    sentences = tree.xpath('//*[@id="bodyContent"]//p/text()')
    sentence = max(sentences, key=lambda s: len(s))
    if len(sentence)>200:
        sentence = sentence[:200]+'...'
    return sentence, page.url

def get_url():
    page = requests.get(url)
    return page.url

def display(i, sentence, url, urls):
    
    random.shuffle(urls)
    print(urls)
    input()
    print(url)

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def ask(urls):
    choices = alphabet[:len(urls)]
    print('Choices:')
    for i in range(len(choices)):
        print(f'{choices[i]}) {urls[i]}')
    choice = input('Enter choice: ').strip()
    if not (choice in choices):
        print(f'"{choice}" is not a valid choice. Try again.')
        return ask(urls)
    i = choices.index(choice)
    return i

N = 4

def turn(i):
    sentence, url = get_sentence()
    urls = [url]
    for _ in range(N-1):
        urls += [get_url()]
    random.shuffle(urls)
    answer = urls.index(url)

    print('~~~~~~~~~~~~~')
    print(f'   Turn {i}')
    print('~~~~~~~~~~~~~')
    print('')
    print('Sentence:')
    print('\t' + sentence)
    print('')
    i = ask(urls)
    if i==answer:
        print("Correct!")
        result = True
    else:
        print(f"The correct choice was {alphabet[answer]}.")
        result = False
    print('')
    return result

INTRO = """~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Wikipedia Guessing Game
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instructions:
- For each turn, a sentence will be shown from a random Wikipedia page.
- Your job is to guess which page it came from.
- You are given 4 choices.
- You have 3 lives.
- Good luck!

"""

OUTRO = """
Thanks for playing! Come back soon :)"""

def evaluation(i):
    if i<10:
        return "you could use some practice."
    elif i<20:
        return "not bad, not bad."
    elif i<40:
        return "alright, that's respectable."
    else:
        return "Well done! Now, you should spend your time doing something else."

def main():
    print(INTRO)

    lives = 3

    i = 1
    while lives>0:
        won = turn(i)
        if not won:
            lives -= 1
            print(f'You have {lives} lives left.\n')
        i += 1

    print(f'Final Score: {i-1}')
    print('...'+evaluation(i-1))

    print(OUTRO)

if __name__=='__main__':
    main()