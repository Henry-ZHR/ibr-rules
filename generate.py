from json import dump
from os import mkdir, path
from shutil import rmtree

RULES_DIR = 'rules'
RULES = {
    'com.tencent.mm': {
        'default': {
            'source': 'intent://extra/rawUrl',
            'ignore': ['qq.com'],
            'force': []
        },
        'QRScanner': {
            'source': 'intent://extra/rawUrl/url',
            'ignore': ['qq.com'],
            'force': []
        }
    },
    'com.tencent.mobileqq': {
        'default': {
            'source': 'intent://extra/url',
            'ignore': ['qq.com'],
            'force': ['weixin.qq.com']
        }
    },
    'com.tencent.wework': {
        'default': {
            'source': 'intent://extra/extra_web_url',
            'ignore': ['work.weixin.qq.com'],
            'force': []
        }
    },
    'tv.danmaku.bili': {
        'default': {
            'source': 'intent://data',
            'ignore': ['bilibili.com', 'b23.tv'],
            'force': []
        }
    },
    'com.mihoyo.hoyolab': {
        'default': {
            'source': 'intent://extra/activity_web_view_url',
            'ignore': ['hoyolab.com', 'mihoyo.com'],
            'force': []
        }
    },
    'com.ss.android.lark': {
        'default': {
            'source': 'intent://extra/url',
            'ignore': ['feishu.cn'],
            'force': []
        }
    }
}


def get_regex_by_domain(domains: list[str]) -> str:
    if len(domains) == 0:
        return ''
    domains_reg = '|'.join(domain.replace('.', r'\.') for domain in domains)
    return ''.join([
        r'https?\:\/\/',  # scheme
        r'([^\/]*\.)?',  # subdomain(s)
        f'({domains_reg})',  # domain(s)
        r'(\/[\s\S]*)?',  # path, etc
    ])


rmtree(RULES_DIR)
mkdir(RULES_DIR)

all_packages = []

for (package_name, rules) in RULES.items():
    all_packages.append(package_name)
    print('Processing: ' + package_name)
    r = {'tag': package_name, 'authors': '', 'rules': []}
    for (tag, attrs) in rules.items():
        r['rules'].append({
            'tag': tag,
            'url-source': attrs['source'],
            'url-filter': {
                'ignore': get_regex_by_domain(attrs['ignore']),
                'force': get_regex_by_domain(attrs['force'])
            }
        })
    with open(path.join(RULES_DIR, package_name + '.json'), 'w') as file:
        dump(r, file, indent=4)

print('Finished writing rules')

s = {'packages': []}
for pkg in all_packages:
    s['packages'].append({'packageName': pkg})
with open('packages.json', 'w') as file:
    dump(s, file, indent=4)
print('Finished writing packages')
