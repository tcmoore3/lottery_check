from bs4 import BeautifulSoup
from urllib2 import urlopen
import ipdb


def get_winning_numbers():
    """Checks the powerball site for the most recent Powerball numbers

    Returns
    -------
    winning_numbers : dict
        A dict containing the white balls and the powerball
    """
    response = urlopen("http://www.powerball.com/powerball/pb_numbers.asp")
    page_source = response.read()
    soup = BeautifulSoup(page_source)
    tables = soup.find('table', attrs={"bordercolor": "#0000FF"})
    rows = tables.find_all('tr')
    cols = rows[1].find_all('td')
    white_balls = [int(col.text.strip()) for col in cols[1:6]]
    powerball = int(cols[7].text.strip())
    return {'white balls': white_balls, 'powerball': powerball}

def check_numbers(numbers, winning_numbers):
    """Check the match between winning numbers and the ticket's numbers
    
    Args
    ----
    numbers : list
        A list of 6 numbers, assumes the powerball is the last number
    winning_numbers : dict
        A dict containing the white balls and the powerball

    This function assumes the powerball is the last number in the list. 
    The order of the other numbers does not matter.

    Returns
    -------

    """
    got_powerball = winning_numbers['powerball'] == numbers[-1]
    matching_numbers = list(set(numbers[:-1]) & set(winning_numbers['white balls']))
    if got_powerball:
        matching_numbers.append(numbers[-1])
    return matching_numbers, got_powerball

def check_ticket(fn):
    import numpy as np
    """Read ticket numbers from a plain text file and find matching number

    Args
    ----
    fn : str
        Name of file containing ticket numbers
    """
    print 'Checking powerball results'
    print '--------------------------'
    numbers = np.loadtxt(fn, dtype=np.int32)
    winning_numbers = get_winning_numbers()
    white_balls = ' '.join([str(x) for x in winning_numbers['white balls']])
    print 'Winning numbers: {0} Powerball: {1}'.format(white_balls,
            winning_numbers['powerball'])
    pb_match = {True: "Powerball match!", False: ' '}
    total_prize = 0
    for row in numbers:
        matches, pb = check_numbers(row, winning_numbers)
        prize = get_prizes(matches, pb)
        total_prize += prize
        if len(matches) == 0:
            print 'No matches'
        else:
            output = ' '.join(str(m) for m in matches) 
            output += ' {0} -> ${1}'.format(pb_match[pb], prize)
            print output
    print 'You won ${0}.'.format(total_prize)

def get_prizes(matching_numbers, powerball_match):
    """Look up the prizes for winning numbers
    """
    prizes = {True: {0: 0, 1: 4, 2: 4, 3: 7, 4: 100, 5: 50000, 6: 'Jackpot!'},
            False: {0: 0, 1: 0, 2: 0, 3: 7, 4: 100, 5: 1000000}}
    return prizes[powerball_match][len(matching_numbers)]
