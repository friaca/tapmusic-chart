from os.path import join, isfile
import sys
from urllib.request import urlopen
import datetime

def get_file_name():
  today = datetime.date.today()
  # If day <= 5, save chart as past month's
  # Fallback to december if month is January
  month = today.month - (today.day <= 5) or 12
  year = today.year

  return '{:02d}-{:02d}.jpg'.format(month, year)

def resolve_duplicate_file(file_path):
  if isfile(file_path):
    expand = 1
    while True:
        expand += 1
        new_file_path = f"{file_path.replace('.jpg', '')}_{str(expand)}.jpg"
        if isfile(new_file_path):
            continue
        else:
            file_path = new_file_path
            break

  return file_path


# ====== Constants ====== #
URL = 'https://tapmusic.net/collage.php?'

PERIODS_MAP = {
  '7 days': '7days',
  '1 month': '1month',
  '3 months': '3months',
  '6 months': '6months',
  '12 months': '12months',
  'overall': 'overall'
}

SIZES_MAP = {
  '3x3': '3x3',
  '4x4': '4x4',
  '5x5': '5x5'
}
# ====== Constants end ====== #

# Set your Last.FM username
username = ''

# On Windows don't forget to scape the slashes: 
# i.e., C:\\Users\\User\\Pictures
download_path = ''

# `period` and `size` are default values, if changed, you may want to 
# change `get_file_name` aswell, because that function only considers 
# the "1 month" period, maybe I'll adapt this is the future...
period = '1 month'
size = '5x5'
captions = True
file_name = get_file_name()

def main():
  if '' in [username, download_path]:
    print('Make sure `download_path` and `username` are filled')
    sys.exit(1)

  if period not in PERIODS_MAP.keys() or size not in SIZES_MAP.keys():
    print('`period` and `size` must be a key of their respective maps')
    sys.exit(1)

  print(f'Downloading a {size} chart for user {username}, from the past {period}...')

  full_path = resolve_duplicate_file(join(download_path, file_name))

  try:
    with open(full_path, 'wb') as file:
      final_url = f'{URL}user={username}&type={PERIODS_MAP[period]}&size={SIZES_MAP[size]}&caption={str(captions).lower()}'

      with urlopen(final_url) as response:
        file.write(response.read())

    print('Downloaded succesfully!')
  except Exception as e:
    print("Couldn't download chart!\n[ERROR] ", e)

if __name__ == '__main__':
  main()
