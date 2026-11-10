"""Keep crawler metadata and text copies aligned with the public pages."""
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://helloredwan.me/'
PERSON = json.loads((ROOT / '_data/person.json').read_text())
PAGES = {
    'index.html': ('Redwan Meslem | Institutional Blockchain & Ethereum Adoption',
                   'Redwan Meslem, Executive Director of the Enterprise Ethereum Alliance, on digital asset strategy, Ethereum protocol research and institutional implementation.', 'ProfilePage'),
    'projects.html': ('Ethereum & Tokenization Projects | Redwan Meslem',
                      'Ethereum tools and research by Redwan Meslem: tokenization, digital identity, agent payments, protocol intelligence and institutional adoption.', 'CollectionPage'),
    'ai-operations.html': ('Running an Organization with Agents | Redwan Meslem',
                           'Redwan Meslem on using agents to coordinate organizational workflows, connect information and keep people responsible for decisions.', 'Article'),
    'speaking-media.html': ('Blockchain & Institutional Finance Talks | Redwan Meslem',
                            'Talks, panels and interviews with Redwan Meslem on Ethereum, institutional blockchain adoption, tokenization and financial infrastructure.', 'CollectionPage'),
    'passport-for-tokenized-markets.html': ('A passport for tokenized markets | Redwan Meslem',
                                           'How shared eligibility credentials could help assets circulate across Ethereum networks.', 'Article'),
    'choosing-ethereum-privacy.html': ('How to choose a privacy solution on Ethereum | Redwan Meslem',
                                      'A practical way to compare privacy options around a real institutional transaction.', 'Article'),
}
ARTICLE_TOPICS = {
    'ai-operations.html': ['Organizational operations', 'AI agents', 'Human oversight'],
    'passport-for-tokenized-markets.html': ['Tokenization', 'Investor eligibility', 'ERC-3643'],
    'choosing-ethereum-privacy.html': ['Ethereum privacy', 'Market infrastructure', 'Institutional adoption'],
}


class MainText(HTMLParser):
    """Export visible main content, including the details readers can expand."""
    def __init__(self, page_url):
        super().__init__()
        self.page_url = page_url
        self.out = []
        self.link_stack = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('h1', 'h2', 'h3'):
            self.out.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag in ('p', 'div', 'section', 'article', 'details', 'summary', 'figure', 'figcaption'):
            self.out.append('\n\n')
        elif tag == 'li':
            self.out.append('\n- ')
        elif tag == 'br':
            self.out.append('\n')
        elif tag == 'a':
            self.out.append('[')
            self.link_stack.append(urljoin(self.page_url, attrs.get('href', '')))

    def handle_endtag(self, tag):
        if tag == 'a' and self.link_stack:
            self.out.append('](' + self.link_stack.pop() + ') ')
        elif tag in ('h1', 'h2', 'h3', 'p', 'div', 'section', 'summary', 'figure', 'figcaption'):
            self.out.append('\n\n')
        elif tag in ('span', 'strong'):
            self.out.append(' ')

    def handle_data(self, value):
        self.out.append(re.sub(r'\s+', ' ', value))

    def text(self):
        result = ''.join(self.out)
        result = re.sub(r'[ \t]+\n', '\n', result)
        result = re.sub(r'\n[ \t]+', '\n', result)
        return re.sub(r'\n{3,}', '\n\n', result).strip() + '\n'


for filename, (title, description, kind) in PAGES.items():
    path = ROOT / filename
    source = path.read_text()
    canonical = BASE if filename == 'index.html' else BASE + filename
    source = re.sub(r'<title>.*?</title>', '<title>' + html.escape(title) + '</title>', source, count=1)
    source = re.sub(r'<meta name="description" content="[^"]*"\s*/?>', '', source)
    source = re.sub(r'\n?<!-- Discovery metadata -->.*?<!-- /Discovery metadata -->\n?', '', source, flags=re.S)
    website = {'@type': 'WebSite', '@id': BASE + '#website', 'name': 'Redwan Meslem', 'url': BASE,
               'publisher': {'@id': PERSON['@id']}, 'inLanguage': 'en'}
    page = {'@type': kind, '@id': canonical + '#page', 'url': canonical, 'name': title,
            'description': description, 'isPartOf': {'@id': website['@id']}, 'inLanguage': 'en'}
    if kind == 'ProfilePage':
        page['mainEntity'] = {'@id': PERSON['@id']}
    elif kind == 'Article':
        headline = ('Running an organization with agents' if filename == 'ai-operations.html'
                    else title.removesuffix(' | Redwan Meslem'))
        page.update(headline=headline, author={'@id': PERSON['@id']}, about=ARTICLE_TOPICS[filename])
    else:
        page['about'] = {'@id': PERSON['@id']}
    schema = {'@context': 'https://schema.org', '@graph': [PERSON, website, page]}
    fields = {
        'description': description, 'author': PERSON['name'],
        'robots': 'index, follow, max-image-preview:large',
        'twitter:card': 'summary_large_image', 'twitter:title': title,
        'twitter:description': description, 'twitter:image': PERSON['image'],
    }
    metadata = ['<!-- Discovery metadata -->']
    metadata.extend('<meta name="' + key + '" content="' + html.escape(value, quote=True) + '">' for key, value in fields.items())
    for key, value in {'og:type': 'article' if kind == 'Article' else 'website',
                       'og:site_name': 'Redwan Meslem', 'og:title': title,
                       'og:description': description, 'og:url': canonical,
                       'og:image': PERSON['image'], 'og:image:alt': 'Redwan Meslem speaking at an event'}.items():
        metadata.append('<meta property="' + key + '" content="' + html.escape(value, quote=True) + '">')
    metadata.extend([
        '<link rel="canonical" href="' + canonical + '">',
        '<link rel="describedby" href="' + BASE + 'llms.txt" type="text/plain">',
        '<link rel="alternate" type="text/markdown" href="' + BASE + filename + '.md" title="Plain-text page">',
        '<script type="application/ld+json">\n' + json.dumps(schema, indent=2).replace('<', '\\u003c') + '\n</script>',
        '<!-- /Discovery metadata -->',
    ])
    source = source.replace('</head>', '\n' + '\n'.join(metadata) + '\n</head>')
    path.write_text(source)
    main = re.search(r'<main\b[^>]*>(.*?)</main>', source, re.S).group(1)
    # Collapse controls are UI copy, not additional profile content.
    main = re.sub(r'<span class="appearance-more">.*?</span></span>', '', main, flags=re.S)
    main = re.sub(r'<(?:div|p) class="(?:overline|portrait-caption)"[^>]*>.*?</(?:div|p)>', '', main, flags=re.S)
    parser = MainText(canonical)
    parser.feed(main)
    (ROOT / (filename + '.md')).write_text(parser.text() + '\nSource: ' + canonical + '\n')

bio = (ROOT / 'aboutme.md').read_text()
bio = re.sub(r'^---\n.*?\n---\n', '# Redwan Meslem\n\n', bio, count=1, flags=re.S)
(ROOT / 'profile.md').write_text(bio)
(ROOT / 'llms.txt').write_text('''# Redwan Meslem

> Executive Director of the Enterprise Ethereum Alliance, working on institutional blockchain adoption, Ethereum, tokenization and open standards.

Redwan connects global institutions with Ethereum teams and decentralized infrastructure. His work covers digital asset strategy, institutional use of blockchain, financial asset tokenization, interoperability, identity and attestations, and agent-payment research. Before EEA, he led developer tooling and infrastructure programs at ChainSafe Systems, including web3.js.

This personal website contains his professional profile, project index, speaking archive and writing. Project descriptions distinguish experiments and research from established standards or production deployments. Public references supporting the biography are linked in the profile.

## Profile and work

- [Professional profile](https://helloredwan.me/profile.md): Biography, background and public references.
- [Homepage](https://helloredwan.me/index.html.md): Current role and professional focus.
- [Projects](https://helloredwan.me/projects.html.md): Ethereum Intelligence, Policy Tracker, Shibui, Rialto, protocol tools and earlier ChainSafe work.
- [Speaking and media](https://helloredwan.me/speaking-media.html.md): Dated appearances, topics, recordings and event links.
- [Running an organization with agents](https://helloredwan.me/ai-operations.html.md): Connecting information and workflows with human ownership and review.
- [A passport for tokenized markets](https://helloredwan.me/passport-for-tokenized-markets.html.md): Shared investor eligibility across Ethereum networks.
- [How to choose a privacy solution on Ethereum](https://helloredwan.me/choosing-ethereum-privacy.html.md): Comparing privacy options for institutional transactions.

## Optional

- [LinkedIn](https://www.linkedin.com/in/redwanmeslem/): Professional profile.
- [GitHub](https://github.com/Redoudou): Public code and projects.
''')
print(f'Updated metadata and text copies for {len(PAGES)} pages, plus profile.md and llms.txt.')
