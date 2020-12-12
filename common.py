# Internal
from settings import settings
from links import Links

# External
import os
import re
import datetime

# To add support for a new asset type to the program,
# change both the asset_types and asset_link_pattern variables.
# Changes in other files may be necessary.

zettel_types = ('.md', '.markdown')
zettel_id_pattern = re.compile(r'(?<!\[\[)\d{14}(?!]])')
asset_types = ('.html', '.jpeg', '.jpg', '.m4a', '.mp4', '.pdf', '.png')
asset_link_pattern = re.compile(r'(?<=]\()(?!https?://|www\d?\.|mailto:|zotero:)(?P<link>.*?(?P<name>[^(/|\\)]*?(\.(html|jpeg|jpg|m4a|mp4|pdf|png))))(?=\))')
web_types = ('.aero', '.arpa', '.biz', '.cat', '.com', '.coop', '.edu', '.firm', '.gov', '.info', '.int', '.jobs', '.mil', '.mobi', '.museum', '.name', '.nato', '.net', '.org', '.pro', '.store', '.travel', '.web', '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.az', '.ax', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cs', '.cu', '.cv', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.htm', '.hu', '.id', '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.sv', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', '.yt', '.yu', '.za', '.zm', '.zw')


# Returns lists of the paths of all zettels and assets in the zettelkasten.
def get_file_paths():
    return get_zettel_paths(), get_asset_paths()


# Returns a list of the paths of all zettels in the zettelkasten.
def get_zettel_paths():
    zettel_paths = []
    zettelkasten_paths = settings.get_zettelkasten_paths()
    for path in zettelkasten_paths:
        os.chdir(path)
        dir_list = os.listdir()

        for file_name in dir_list:
            if file_name.endswith(zettel_types):
                file_name = os.path.abspath(file_name)
                zettel_paths.append(file_name)

    return zettel_paths


# Returns a list of the paths of all assets in the zettelkasten.
def get_asset_paths():
    asset_paths = []
    asset_dir_paths = settings.get_asset_dir_paths()
    for path in asset_dir_paths:
        os.chdir(path)
        dir_list = os.listdir()

        for file_name in dir_list:
            if file_name.endswith(asset_types):
                file_name = os.path.abspath(file_name)
                asset_paths.append(file_name)

    return asset_paths


# Get the title of one zettel (the first header level 1).
def get_zettel_title(zettel_path):
    path_list = []
    path_list.append(zettel_path)
    title_list = get_zettel_titles(path_list)
    return title_list[0]


# Get the titles of each of a list of zettels.
# The title of a zettel is its first header level 1.
def get_zettel_titles(zettel_paths):
    zettel_titles = []
    title_pattern = re.compile(r'(?<![^\n])# .+')
    for zettel_path in zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        title = title_pattern.search(contents)
        if title is not None:
            title = title[0][2:]  # Remove the '# ' from the title.
            zettel_titles.append(title)

    return zettel_titles


# Determine whether a link is a URL.
# Can give false positives for some types of file links,
# but gives the correct answer for html links (whether URL or not).
def is_URL(link):
    for web_type in web_types:
        if web_type in link:
            if link.endswith('.html'):
                if (web_type == '.ht' or web_type == '.htm') and link.count(web_type) > 1:
                    return True
                else:
                    return False
            else:
                return True
    return False


# Get all the links in one zettel.
# contents is a string.
def get_asset_links(contents):
    links = Links()
    for link_match in re.finditer(asset_link_pattern, contents):
        link_dict = link_match.groupdict()

        # Ignore web URLs that end with '.html', but not locally saved .html files.
        if link_dict['link'].endswith('.html'):
            if is_URL(link_dict['link']):
                continue

        links.append(link_dict['link'], link_dict['name'])

    return links


# Generate a 14-digit zettel ID that represents the current date and time
# (the format is YYYYMMDDhhmmss).
def generate_zettel_id():
    zettel_id = str(datetime.datetime.now())
    zettel_id = zettel_id[:19]  # Remove the microseconds.
    zettel_id = zettel_id.replace('-', '').replace(':', '').replace(' ', '')
    return zettel_id


# Find the 14-digit ID of a zettel (the format is YYYYMMDDhhmmss).
# The zettel ID can be in the file name or in the file's contents.
def find_zettel_id(zettel_path):
    # Search for the zettel ID in the file's name.
    zettel_name = os.path.split(zettel_path)[1]
    zettel_id_match = zettel_id_pattern.search(zettel_name)
    if zettel_id_match is None:
        # Search for the zettel ID in the zettel's contents.
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        zettel_id_match = zettel_id_pattern.search(contents)
        if zettel_id_match is None:
            # This zettel has no ID.
            return -1

    return zettel_id_match[0]


# Get the zettelkasten-style link to a zettel, in the format:
# '[[20201215093128]] This is the zettel title'
def get_zettel_link(zettel_path):
    zettel_id = find_zettel_id(zettel_path)
    if zettel_id == -1:
        raise ValueError('Zettel ID not found.')

    zettel_title = get_zettel_title(zettel_path)
    zettel_link = '[[' + zettel_id + ']] ' + zettel_title

    return zettel_link
