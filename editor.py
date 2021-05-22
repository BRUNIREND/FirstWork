# write your code here

def reformat(format):
    global asks
    if format == maby_asks[0]:
        text = input('Text: ')
        asks += text
        return asks
    elif format == maby_asks[1]:
        text = input('Text: ')
        asks += f'**{text}**'
        return asks
    elif format == maby_asks[2]:
        text = input('Text: ')
        asks += f'*{text}*'
        return asks
    elif format == maby_asks[3]:
        levels = int(input('Level: '))
        if levels > 6 or levels < 1:
            return 'The level should be within the range of 1 to 6'
        text = input('Text: ')
        asks += '#' * levels + ' ' + text + '\n'
        return asks
    elif format == maby_asks[4]:
        label = input('Label: ')
        url = input('URL: ')
        asks += f'[{label}]({url})'
        return asks
    elif format == maby_asks[5]:
        text = input('Text: ')
        asks += f'`{text}`'
        return asks
    elif format == maby_asks[6]:
        asks += '\n'
        return asks
    elif format == maby_asks[7]:


        while True:
            number_rows = int(input('Number of rows: '))
            if number_rows > 0:
                break
            else:
                print('The number of rows should be greater than zero')
        for i in range(number_rows):

            asks += str(i + 1) + '. ' + input(f'Row #{i+1}: ') + '\n'
        return asks
    elif format == maby_asks[8]:

        while True:
            number_rows = int(input('Number of rows: '))
            if number_rows > 0:
                break
            else:
                print('The number of rows should be greater than zero')
        for i in range(number_rows):
            asks += '* ' + input(f'Row #{i + 1}: ') + '\n'
        return asks

asks = ''

maby_asks = ["plain",
             "bold",
             "italic",
             "header",
             "link",
             "inline-code",
             "new-line",
             'ordered-list',
             'unordered-list']


while True:
    user_input = input("Choose a formatter: ")
    if user_input == '!help':
        print('Available formatters: plain bold italic header link inline-code new-line\nSpecial commands: !help !done ')
    elif user_input == '!done':
        with open('output.md', 'w') as f:
            f.write(asks)
        break
    elif user_input in maby_asks:
        print(reformat(user_input))

    else:
        print('Unknown formatting type or command')
    
print(
"""
# John Lennon
or ***John Winston Ono Lennon*** was one of *The Beatles*.
Here are the songs he wrote I like the most:
* Imagine
* Norwegian Wood
* Come Together
* In My Life
* ~~Hey Jude~~ (that was *McCartney*)
""")