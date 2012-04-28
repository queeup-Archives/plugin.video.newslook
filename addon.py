# -*- coding: utf-8 -*-

# Imports
import sys
import urllib
import simplejson
import time
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

# Debug
DEBUG = False

__addon__ = xbmcaddon.Addon(id='plugin.video.newslook')
__info__ = __addon__.getAddonInfo
__plugin__ = __info__('name')
__version__ = __info__('version')
__icon__ = __info__('icon')
__language__ = __addon__.getLocalizedString

URL = 'http://iptv.newslook.com/api/v2/categories/%s.json'


class Main:
  def __init__(self):
    # create playlist for play all
    self.plist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    # clean playlist
    self.plist.clear()
    if DEBUG:
      self.log('cleaning playlist before adding new content')
    if ("action=list" in sys.argv[2]):
      self.list_contents(self.arguments('url'))
    elif ("action=playall" in sys.argv[2]):
      self.play_all()
    else:
      self.main_menu()

  def main_menu(self):
    if DEBUG:
      self.log('main_menu()')
    menu = [{'title':__language__(30201), 'url':URL % 'top-news'},
            {'title':__language__(30202), 'url':URL % 'world'},
            {'title':__language__(30203), 'url':URL % 'u-s-news'},
            {'title':__language__(30204), 'url':URL % 'finance'},
            {'title':__language__(30205), 'url':URL % 'science'},
            {'title':__language__(30206), 'url':URL % 'technology'},
            {'title':__language__(30207), 'url':URL % 'health-medicine'},
            {'title':__language__(30208), 'url':URL % 'artsculture'},
            {'title':__language__(30209), 'url':URL % 'lifestyle'}]
    for title in menu:
      listitem = xbmcgui.ListItem(title['title'], iconImage='DefaultFolder.png', thumbnailImage=__icon__)
      url = '%s?action=list&url=%s' % (sys.argv[0], urllib.quote_plus(title['url']))
      xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(url, listitem, True)])
    # Sort methods and content type...
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
    # End of directory...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def list_contents(self, url):
    if DEBUG:
      self.log('list_contents()')
    # Play all at once directory item
    listitem = xbmcgui.ListItem('▶ Play All', iconImage='NowPlayingIcon.png')
    parameters = '%s?action=playall' % (sys.argv[0])
    xbmcplugin.addDirectoryItem(int(sys.argv[1]), parameters, listitem, True)
    json = simplejson.loads(urllib.urlopen(url).read())
    for entry in json['videos']:
      _id = entry['id']
      title = entry['title']
      description = entry['description']
      _duration = entry['duration']
      if _duration >= 3600 * 1000:
          duration = time.strftime('%H:%M:%S', time.gmtime(_duration / 1000))
      else:
        duration = time.strftime('%M:%S', time.gmtime(_duration / 1000))
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
                                   'duration': duration})
      xbmcplugin.addDirectoryItems(int(sys.argv[1]), [(video, listitem, False)])
      # add all contents to playlist for playall
      self.plist.add(video, listitem)
    # Content Type
    xbmcplugin.setContent(int(sys.argv[1]), 'movies')
    # Sort methods
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE, label2Mask='%D')
    # End of directory...
    xbmcplugin.endOfDirectory(int(sys.argv[1]), True)

  def play_all(self):
    if DEBUG:
      self.log('play_all()')
    xbmcPlayer = xbmc.Player()
    xbmcPlayer.play(self.plist)

  def arguments(self, arg, unquote=True):
    _arguments = dict(part.split('=') for part in sys.argv[2][1:].split('&'))
    if unquote:
      return urllib.unquote_plus(_arguments[arg])
    else:
      return _arguments[arg]

  def log(self, description):
    xbmc.log("[ADD-ON] '%s v%s': DEBUG: %s" % (__plugin__, __version__, description), xbmc.LOGNOTICE)

if __name__ == '__main__':
  Main()