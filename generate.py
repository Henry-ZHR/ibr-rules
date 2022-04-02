from json import dump
from os import mkdir, path
from shutil import rmtree

RULES_DIR = 'rules'
RULES = {
    'com.tencent.mm': {
        'default': {
            'source': 'intent://extra/rawUrl',
            'ignore': ['qq.com'],
            'force': ['']
        },
        'QRScanner': {
            'source': 'intent://extra/rawUrl/url',
            'ignore': ['qq.com'],
            'force': ['']
        }
    },
    'com.tencent.mobileqq': {
        'default': {
            'source': 'intent://extra/url',
            'ignore': ['qq.com'],
            'force': ['weixin.qq.com']
        }
    },
    'tv.danmaku.bili': {
        'default': {
            'source': 'intent://data',
            'ignore': ['bilibili.com', 'b23.tv'],
            'force': []
        }
    },
    'com.tencent.androidqqmail': {
        'default': {
            'source': 'intent://extra/url',
            'ignore': [],
            'force': []
        }
    },
    'com.mihoyo.hoyolab': {
        'default': {
            'source': 'intent://extra/activity_web_view_url',
            'ignore': ['hoyolab.com'],
            'force': []
        }
    }
}


def get_regex_by_domain(domains: list[str]) -> str:
    if len(domains) == 0:
        return ''
    return 'https?\\:\\/\\/([^\\/]+\\.|)(%s)(\\/.*)?' % '|'.join(
        domain.replace('.', '\\.') for domain in domains)


if path.isdir(RULES_DIR):
    input('Rules directory already exists. Press Enter to delete it...')
    rmtree(RULES_DIR)

mkdir(RULES_DIR)

for (packageName, rules) in RULES.items():
    print('Processing: ' + packageName)
    r = {'tag': packageName, 'authors': '', 'rules': []}
    for (tag, attrs) in rules.items():
        r['rules'].append({
            'tag': tag,
            'url-source': attrs['source'],
            'url-filter': {
                'ignore': get_regex_by_domain(attrs['ignore']),
                'force': get_regex_by_domain(attrs['force'])
            }
        })
    file = open(path.join(RULES_DIR, packageName + '.json'), 'w')
    dump(r, file)
    file.close()

print('Done')