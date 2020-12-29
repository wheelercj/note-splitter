# External imports
import os
import re
import yaml

'''
To add support for a new asset type to the program, change:
* asset_types (below)
* asset_link_pattern (below)
* the list of supported file types in the README
'''
zettel_types = ('.md')  # Changing zettel_types will require changes in several other places if the new zettel type has a different length.
zettel_id_pattern = re.compile(r'(?<!\[\[)\d{14}(?!]])')
asset_types = ('.html', '.jpeg', '.jpg', '.m4a', '.mp4', '.pdf', '.png')
asset_link_pattern = re.compile(r'(?<=]\()(?!https?://|www\d?\.|mailto:|zotero:|obsidian:)(?P<link>.*?(?P<name>[^(/|\\)]*?(\.(html|jpeg|jpg|m4a|mp4|pdf|png))))(?=\))')
web_types = ('.ac', '.ad', '.ae', '.aero', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.arpa', '.as', '.at', '.au', '.aw', '.ax', '.az', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.biz', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cat', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.com', '.coop', '.cr', '.cs', '.cu', '.cv', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.edu', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.firm', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gov', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.hu', '.id', '.ie', '.il', '.im', '.in', '.info', '.int', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jobs', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.mg', '.mh', '.mil', '.mk', '.ml', '.mm', '.mn', '.mo', '.mobi', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.museum', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.name', '.nato', '.nc', '.ne', '.net', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.org', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.pro', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.store', '.sv', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.travel', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.web', '.wf', '.ws', '.ye', '.yt', '.yu', '.za', '.zm', '.zw')


def load_settings():
    with open('user_settings.yaml', 'r') as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def save_settings(settings):
    with open('user_settings.yaml', 'w') as file:
        yaml.dump(settings, file)


# Return a dict of the default settings.
def default_settings():
    settings = dict()
    settings['zk_paths'] = []  # Zettelkasten paths.
    settings['ad_paths'] = []  # Asset directory paths.
    settings['dl_paths'] = []  # Downloads paths.

    return settings


# Convert the tuple of asset types into a readable sentence.
def get_asset_types_str():
    asset_types_list = []
    for asset_type in asset_types:
        asset_types_list.append(asset_type[1:])
    asset_types_str = ', '.join(asset_types_list)
    split_types = asset_types_str.rsplit(', ', 1)
    asset_types_str = split_types[0] + ', and ' + split_types[1]

    return asset_types_str


# Check whether all the filepaths in the given list are absolute.
def all_abs(paths):
    for path in paths:
        if not path == '' and not os.path.isabs(path):
            return False
    return True
