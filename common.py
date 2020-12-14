# Internal
from settings import settings
from links import Links

# External
import os
import re
import datetime

'''
To add support for a new asset type to the program, change:
* asset_types (below)
* asset_link_pattern (below)
* the list of supported file types in the README
'''

zettel_types = ('.md')
zettel_id_pattern = re.compile(r'(?<!\[\[)\d{14}(?!]])')
asset_types = ('.html', '.jpeg', '.jpg', '.m4a', '.mp4', '.pdf', '.png')
asset_link_pattern = re.compile(r'(?<=]\()(?!https?://|www\d?\.|mailto:|zotero:)(?P<link>.*?(?P<name>[^(/|\\)]*?(\.(html|jpeg|jpg|m4a|mp4|pdf|png))))(?=\))')
web_types = ('.ac', '.ad', '.ae', '.aero', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.arpa', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.biz', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cat', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.com', '.coop', '.cr', '.cs', '.cu', '.cv', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.edu', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.firm', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gov', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', '.in', '.info', '.int', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jobs', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.mg', '.mh', '.mil', '.mk', '.ml', '.mm', '.mn', '.mo', '.mobi', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.museum', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.name', '.nato', '.nc', '.ne', '.net', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.org', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.pro', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.store', '.sv', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.travel', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.web', '.wf', '.ws', '.ye', '.yt', '.yu', '.za', '.zm', '.zw')


# Return two lists of paths of all zettels and assets in the
# zettelkasten and assets folders chosen in settings.
def get_file_paths():
    return get_zettel_paths(), get_asset_paths()


# Return a list of paths of all zettels in the
# zettelkasten folders chosen in settings.
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


# Return a list of paths of all assets in the
# assets folders chosen in settings.
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
    with open(zettel_path, 'r', encoding='utf8') as zettel:
        contents = zettel.read()
    title_match = re.search(r'(?<![^\n])# .+', contents)
    if title_match is not None:
        return title_match[0][2:]  # Remove the '# ' from the title.
    else:
        return ''


# Get the titles of each of a list of zettels.
# The title of a zettel is its first header level 1.
def get_zettel_titles(zettel_paths):
    zettel_titles = []
    title_pattern = re.compile(r'(?<![^\n])# .+')

    for zettel_path in zettel_paths:
        with open(zettel_path, 'r', encoding='utf8') as zettel:
            contents = zettel.read()
        title_match = title_pattern.search(contents)
        if title_match is not None:
            title = title_match[0][2:]  # Remove the '# ' from the title.
            zettel_titles.append(title)

    return zettel_titles


# Determine whether a link that ends with '.html' or
# '.htm' is a URL (or a local file link).
def html_link_is_URL(link):
    if link.count('.ht') > 1:
        return True
    else:
        for web_type in web_types:
            if web_type != '.ht' and web_type in link:
                return True
        return False


# Return a Links object of all the asset links in one zettel.
# The links returned are all of a type in asset_types; all
# other link types are ignored.
# contents is a string.
# zettel_path is the abs path of the zettel that contains the
# asset links, and is only needed if there are relative asset links.
def get_asset_links(contents, zettel_path):
    links = Links()
    for link_match in re.finditer(asset_link_pattern, contents):
        link_dict = link_match.groupdict()

        # URLs that end with '.html' or '.htm' could be in the list.
        # Ignore them, but not locally saved files with those endings.
        if link_dict['link'].endswith('.html') or link_dict['link'].endswith('.htm'):
            if html_link_is_URL(link_dict['link']):
                continue

        links.append(link_dict['link'], link_dict['name'], zettel_path)

    return links


# Generate a 14-digit zettel ID that represents the current date and time
# (the format is YYYYMMDDhhmmss).
def generate_zettel_id():
    zettel_id = str(datetime.datetime.now())
    zettel_id = zettel_id[:19]  # Remove the microseconds.
    zettel_id = zettel_id.replace('-', '').replace(':', '').replace(' ', '')
    return zettel_id


# Return the ID of a zettel. This function looks for a 14-digit number
# first in the file name and then in its contents, and only uses the
# file's full name as the ID if it can't find the 14-digit number.
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
            # The zettel ID is not a 14-digit number,
            # it's the name of the file.
            return os.path.split(zettel_path)[-1][:-3]

    return zettel_id_match[0]


# Return the zettelkasten-style link to a zettel, such as:
# '[[20201215093128]] This is the zettel title'.
def get_zettel_link(zettel_path):
    zettel_id = find_zettel_id(zettel_path)
    zettel_title = get_zettel_title(zettel_path)
    zettel_link = '[[' + zettel_id + ']] ' + zettel_title

    return zettel_link
