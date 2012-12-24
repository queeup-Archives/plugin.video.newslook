# -*- coding: utf-8 -*-

# Imports
import sys
import urllib
import urlparse
import simplejson
#import time
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# Debug
DEBUG = False

__addon__ = xbmcaddon.Addon()
__plugin__ = __addon__.getAddonInfo('name')
__version__ = __addon__.getAddonInfo('version')
__icon__ = __addon__.getAddonInfo('icon')

URL = 'http://iptv.newslook.com/api/v2/categories/%s.json'
CATEGORIES = 'http://iptv.newslook.com/api/v2/categories.json'


class Main:
  def __init__(self):
    # create playlist for play all
    self.plist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    if ("action=list" in sys.argv[2]):
      self.list_contents(self.parameters('url'))
    elif ("action=playall" in sys.argv[2]):
      self.play_all()
    else:
      self.main_menu()

  def main_menu(self):
    if DEBUG:
      self.log('main_menu()')
    categories_json = simplejson.loads(urllib.urlopen(CATEGORIES).read())
    for categories in categories_json['categories']:
      name = categories['name']
      permalink = categories['permalink']
      listitem = xbmcgui.ListItem(name, iconImage='DefaultFolder.png', thumbnailImage=__icon__)
      url = sys.argv[0] + '?' + urllib.urlencode({'action': 'list',
                                                  'url': URL % permalink})
      xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(url, listitem, True)])
    # Sort methods and content type...
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
    # End of directory...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def list_contents(self, category_url):
    if DEBUG:
      self.log('list_contents()')
    if DEBUG:
      self.log('cleaning playlist before adding new content')
    # clean playlist
    self.plist.clear()
    # Play all at once directory item
    listitem = xbmcgui.ListItem('▶ Play All', iconImage='NowPlayingIcon.png')
    url = sys.argv[0] + '?' + urllib.urlencode({'action': 'playall'})
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, listitem, True)
    json = simplejson.loads(urllib.urlopen(category_url).read())
    for entry in json['videos']:
      _id = entry['id']
      title = entry['title']
      description = entry['description']
      #_duration = entry['duration']
      #if _duration >= 3600 * 1000:
      #    duration = time.strftime('%H:%M:%S', time.gmtime(_duration / 1000))
      #else:
      #  duration = time.strftime('%M:%S', time.gmtime(_duration / 1000))
      video = entry['cdn_asset_url']
      #channel = entry['channel_name']
      thumbnail_version = entry['thumbnail_version']
      thumbnail = 'http://img1.newslook.com/images/dyn/videos/%s/%s/pad/324/231/%s.jpg' % (_id, thumbnail_version, _id)

      listitem = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=thumbnail)
      listitem.setProperty('IsPlayable', 'true')
      listitem.setProperty('mimetype', 'video/mp4')
      listitem.setInfo(type='video',
                       infoLabels={'title': title,
                                   'plot': description,
                                   #'duration': duration,
                                   })
      xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(video, listitem, False)])
      # add all contents to playlist for playall
      self.plist.add(video, listitem)
    # Content Type
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    # Sort methods
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
    # End of directory...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def play_all(self):
    if DEBUG:
      self.log('play_all()')
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(self.plist)

  def parameters(self, arg):
    _parameters = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)
    return _parameters[arg][0]

  def log(self, description):
    xbmc.log("[ADD-ON] '%s v%s': DEBUG: %s" % (__plugin__, __version__, description), xbmc.LOGNOTICE)

if __name__ == '__main__':
  Main()