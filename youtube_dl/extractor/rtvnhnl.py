# coding: utf-8
from __future__ import unicode_literals

from .common import InfoExtractor


class RtvnhNlIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?rtvnh\.nl/video/(?P<id>[0-9]+)'
    _TEST = {
        'params': {
            'hls_prefer_native': True
        },

        'url': 'http://www.rtvnh.nl/video/131946',
        'md5': '6e1d0ab079e2a00b6161442d3ceacfc1',
        'info_dict': {
            'id': '131946',
            'ext': 'mp4',
            'title': 'Grote zoektocht in zee bij Zandvoort naar vermiste vrouw',
            'thumbnail': 're:^https?://rtvnh-webfiles\.[^.]+\.amazonaws\.com/data/cache/[0-9]+/basedata/pf_image/[0-9.]+/[0-9\-a-f]+\.jpg$'
        }
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        meta = self._parse_json(self._download_webpage('http://www.rtvnh.nl/video/json?m=' + video_id, video_id), video_id)
        formats = self._extract_smil_formats('http://www.rtvnh.nl/video/smil?m=' + video_id, video_id)

        for item in meta['source']['fb']:
            if item.get('type') == 'hls':
                formats.extend(self._extract_m3u8_formats(item['file'], video_id, ext='mp4'))
            elif item.get('type') == '':
                formats.append({'url': item['file']})
        
        return {
            'id': video_id,
            'title': meta['title'].strip(),
            'thumbnail': meta['image'],
            'formats': formats
        }
