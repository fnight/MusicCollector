import argparse
import requests
import sys
import re
import codecs


def main(argv):

    if len(argv) < 4:
        print("VKMusicCollector is using rutracker.cr to download songs, therefore this options are required\n")
        print("       -b: Band name")
        print("       -s: Song name")
        print("       -u: Rutracker username")
        print("       -p: Rutracker password")

    parser = argparse.ArgumentParser(description = 'VKMusicCollector is using rutracker.cr to download songs, '
                                                   'therefore this options are required:\n'
                                                   '\t-b: Band name\n'
                                                   '\t-s: Song name\n'
                                                   '\t-u: Rutracker username\n'
                                                   '\t-p: Rutracker password\n')
    parser.add_argument('username', type = str)
    parser.add_argument('password', type = str)
    parser.add_argument('-b', '--band', type = str, nargs = '+', required=True, action = 'append')
    parser.add_argument('-s', '--song', type = str, nargs = '+', required=True, action = 'append')
    args = parser.parse_args()
    band = ' '.join(args.band[0])
    song = ' '.join(args.song[0])
    username = args.username
    password = args.password

    # opts, args = getopt.getopt(argv, "b:s:u:p:")
    # for opt, arg in opts:
    #     if opt == '-b':
    #         band = arg
    #     elif opt == '-s':
    #         song = arg
    #     elif opt == '-u':
    #         username = arg
    #     elif opt == '-p':
    #         password = arg

    session = requests.Session()

    # signing in
    print('Signing in...')
    url = 'http://rutracker.cr/forum/login.php'
    values = {'login_username': username, 'login_password': password, 'login': 'Вход'}
    session.post(url, data = values)

    # making search request
    print('Searching...')
    band = re.sub(r'( )+$', '', band)
    band = re.sub(r' +', '%20', band)
    urly = "http://rutracker.cr/forum/tracker.php?f=1126,1128,1130,1132,1134,1136,1138,1172,1173,1219,1221,1223,1225," \
           "1226,1282,1283,1284,1331,1334,1361,1362,1396,1635,1703,1705,1707,1709,1711,1713,1715,1725,1727,1729,1731," \
           "1737,1739,1741,1743,1745,1747,1749,1764,1765,1766,1767,1769,1770,1771,1772,1773,1778,1780,1797,1799,1816," \
           "1819,1822,1826,1828,1830,1847,1856,1858,1895,2018,2084,2174,2231,2287,2288,2295,2298,2309,2310,2311,2330," \
           "2331,2431,2501,2503,424,428,436,441,446,463,466,469,738,740,783,785,796,798,880,952,965,969&nm=" + \
           band + '%20-lossless'

    r1 = session.get(urly)
    text = re.sub('windows-1251', 'utf-8', r1.text)
    # with codecs.open("Response1.html", "w", "utf-8-sig") as temp:
    #     temp.write(text)
    link_list = re.findall(r'<a(.*)(class="med tLink hl-tags bold")(.*)>(.*)</a>', text)
    href_list = [re.search(r'href(.*)=(.*)"(.*)"', x[2]).group(0) for x in link_list]
    href_list = [re.sub(r'(.*)href="( *)', '', x) for x in href_list]
    href_list = [re.sub(r'( *)"( *)', '', x) for x in href_list]
    href_list = ['http://rutracker.cr/forum/' + x for x in href_list]

    print('Found ' + str(len(href_list)) + ' links:')
    for x in href_list:
        print('\t' + x)
    print('Parsing links...')

    for x in href_list:
        data = {'t': re.search(r'[0-9]+$', x).group(0)} #for POST requests
        # r2 = session.get(x)
        r3 = session.post('http://rutracker.cr/forum/viewtorrent.php', data = data)

    # r2 = session.get(href_list[0])
    # text = re.sub('windows-1251', 'utf-8', r2.text)
    # with codecs.open("Response2.html", "w", "utf-8-sig") as temp:
    #     temp.write(text)

    # r3 = session.post('http://rutracker.cr/forum/viewtorrent.php', data = {'t': re.search(r'[0-9]+$', href_list[0]).group(0) } )
    # text = re.sub('windows-1251', 'utf-8', r3.text)
    # with codecs.open("Response3.html", "w", "utf-8-sig") as temp:
    #     temp.write(text)

    # r'<a data-topic_id="" class="med tLink hl-tags bold" href="viewtopic.php?t=5140112">(Pop,) VA (Sex Pistols, ' \
    # r'Daft Punk, Bastille, Mike Oldfield, Massive Attack, Enigma, deadmau5 и др.) - Virgin Records: 40 Years of ' \
    # r'Disruptions - 2013, MP3, 320 kbps</a> '

    # with open('Response.html', 'w') as file:
    #     file.write(text)
    sys.exit()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("Search interrupted by user..")
    except Exception as e:
        print("-------wooops-------")
        print(e)
        sys.exit()
