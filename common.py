# This file is imported by a few other files.

import os
import re

zettelkasten_paths = {
    'C:/Users/chris/Documents/Zettelkasten'
}
asset_dir_paths = {
    'C:/Users/chris/Documents/Zettelkasten',
    'C:/Users/chris/Documents/Zettelkasten/assets'
}

zettel_types = ('.md', '.markdown')
zettel_type_pattern = r'\.(md|markdown)'
asset_types = ('.jpg', '.jpeg', '.png', '.pdf', '.mp4', '.html')
asset_link_pattern = re.compile(r'(?<=]\()(?!https?://|www\d?\.|mailto:|zotero:)(?P<link>.*?(?P<name>[^(/|\\)]*?(\.(jpg|jpeg|png|pdf|mp4|html))))(?=\))')
web_types = ('.aero', '.arpa', '.biz', '.cat', '.com', '.coop', '.edu', '.firm', '.gov', '.info', '.int', '.jobs', '.mil', '.mobi', '.museum', '.name', '.nato', '.net', '.org', '.pro', '.store', '.travel', '.web', '.ac', '.ad', '.ae', '.af', '.ag', '.ai', '.al', '.am', '.an', '.ao', '.aq', '.ar', '.as', '.at', '.au', '.aw', '.az', '.ax', '.ba', '.bb', '.bd', '.be', '.bf', '.bg', '.bh', '.bi', '.bj', '.bm', '.bn', '.bo', '.br', '.bs', '.bt', '.bv', '.bw', '.by', '.bz', '.ca', '.cc', '.cd', '.cf', '.cg', '.ch', '.ci', '.ck', '.cl', '.cm', '.cn', '.co', '.cr', '.cs', '.cu', '.cv', '.cx', '.cy', '.cz', '.de', '.dj', '.dk', '.dm', '.do', '.dz', '.ec', '.ee', '.eg', '.eh', '.er', '.es', '.et', '.eu', '.fi', '.fj', '.fk', '.fm', '.fo', '.fr', '.ga', '.gb', '.gd', '.ge', '.gf', '.gg', '.gh', '.gi', '.gl', '.gm', '.gn', '.gp', '.gq', '.gr', '.gs', '.gt', '.gu', '.gw', '.gy', '.hk', '.hm', '.hn', '.hr', '.ht', '.htm', '.hu', '.id', '.ie', '.il', '.im', '.in', '.io', '.iq', '.ir', '.is', '.it', '.je', '.jm', '.jo', '.jp', '.ke', '.kg', '.kh', '.ki', '.km', '.kn', '.kp', '.kr', '.kw', '.ky', '.kz', '.la', '.lb', '.lc', '.li', '.lk', '.lr', '.ls', '.lt', '.lu', '.lv', '.ly', '.ma', '.mc', '.md', '.mg', '.mh', '.mk', '.ml', '.mm', '.mn', '.mo', '.mp', '.mq', '.mr', '.ms', '.mt', '.mu', '.mv', '.mw', '.mx', '.my', '.mz', '.na', '.nc', '.ne', '.nf', '.ng', '.ni', '.nl', '.no', '.np', '.nr', '.nu', '.nz', '.om', '.pa', '.pe', '.pf', '.pg', '.ph', '.pk', '.pl', '.pm', '.pn', '.pr', '.ps', '.pt', '.pw', '.py', '.qa', '.re', '.ro', '.ru', '.rw', '.sa', '.sb', '.sc', '.sd', '.se', '.sg', '.sh', '.si', '.sj', '.sk', '.sl', '.sm', '.sn', '.so', '.sr', '.st', '.sv', '.sy', '.sz', '.tc', '.td', '.tf', '.tg', '.th', '.tj', '.tk', '.tl', '.tm', '.tn', '.to', '.tp', '.tr', '.tt', '.tv', '.tw', '.tz', '.ua', '.ug', '.uk', '.um', '.us', '.uy', '.uz', '.va', '.vc', '.ve', '.vg', '.vi', '.vn', '.vu', '.wf', '.ws', '.ye', '.yt', '.yu', '.za', '.zm', '.zw')


# Returns lists of the paths of all zettels and assets in the zettelkasten.
def get_file_paths():
    return get_zettel_paths(), get_asset_paths()


# Returns a list of the paths of all zettels in the zettelkasten.
def get_zettel_paths():
    zettel_paths = []
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
    for path in asset_dir_paths:
        os.chdir(path)
        dir_list = os.listdir()

        for file_name in dir_list:
            if file_name.endswith(asset_types):
                file_name = os.path.abspath(file_name)
                asset_paths.append(file_name)

    return asset_paths


# Determine whether a link is a URL.
# Can give false positives for some types of file links,
# but gives the correct answer for html links (whether URL or not).
def is_URL(link):
    for web_type in web_types:
        if web_type in link:
            if link.endswith('.html'):
                if web_type == '.ht' or web_type == '.htm' and link.count(web_type) > 1:
                    return True
                else:
                    return False
            else:
                return True
    return False
