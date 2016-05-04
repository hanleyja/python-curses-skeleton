#!/usr/bin/env python2

#  Jesse Hanley - 2016
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

# This is inteded as a framework for a simple python program with
# curses support.  For the example, it just lists information about
# CPUs on the machine

from __future__ import division # Requires Python 2.2 or later
from __future__ import with_statement # Requires Python 2.5 or later
from __future__ import unicode_literals # Requires Python 2.6 or later
from __future__ import print_function # Requires Python 2.6 or later

import sys, os, os.path, traceback, platform
import argparse
import time, re, glob
import curses
import curses.textpad

__author__ = "Jesse Hanley"
__credits__ = ["Jesse Hanley"]
__version__ = "0.1"
__maintainer__ = "Jesse Hanley"
__email__ = "hanleyja@users.noreply.github.com"
__progname__ = "python-curses-skeleton"
__year__ = 2016

def display(screen):
  global settings
  screen.clear()
  max_y, max_x = screen.getmaxyx()  ## 51, 204 for just mac laptop
  y = 0

  ## Sanity Checks
  if settings is None:
    return
  if 'compact' not in settings: # should always exist
    return

  try:
    with open('/proc/cpuinfo', 'r') as cpuinfo:
      for line in cpuinfo:
        if line.startswith('processor'):
          screen.addstr(y, 2, "{0}".format(line))
          y += 1
        elif settings['compact'] >= 2 and line.startswith('model name'):
          screen.addstr(y, 4, "{0}".format(line))
          y += 1
        elif settings['compact'] >= 3 and line.startswith('flags'):
          screen.addstr(y, 4, "{0}".format(line))
          y += 1
  except IOError as e:
    print('Cannot open CPU info')
  
  screen.refresh()
  
  return

def display_help(screen):
  screen.clear()
  max_y, max_x = screen.getmaxyx()
  y = 0

  screen.addstr(y, 2, "{0} {1} - (C) {2} {3}".format(__progname__, __version__, __year__, __author__), curses.color_pair(15))
  y += 3
  
  ## ? or h
  screen.addstr(y, 2, "{0:<12}".format("? or h"), curses.color_pair(7))
  screen.addstr(y, 15, "This menu")
  y += 1

  ## c
  screen.addstr(y, 2, "{0:<12}".format("c"), curses.color_pair(7))
  screen.addstr(y, 15, "Clear the screen")
  y += 1
  
  ## z
  screen.addstr(y, 2, "{0:<12}".format("z"), curses.color_pair(7))
  screen.addstr(y, 15, "Collapse information.  Press again to increment collapse amount")
  y += 1

  ## Z
  screen.addstr(y, 2, "{0:<12}".format("Z"), curses.color_pair(7))
  screen.addstr(y, 15, "Uncollapse information.  Press again to decrease collapse amount")
  y += 1
  
  ## q
  screen.addstr(y, 2, "{0:<12}".format("q"), curses.color_pair(7))
  screen.addstr(y, 15, "Quit")
  y += 1

  screen.refresh()

def main(screen):
  global settings
  screen.clear()
  curses.start_color()
  curses.use_default_colors()
  screen.scrollok(False)

  maxcompact = 3
  mincompact = 1

  ## Some sane defaults
  settings = {
    'compact'       : 1,
    'helptoggle'    : False,
  }

  for i in range(0, curses.COLORS):
    curses.init_pair(i + 1, i, -1)
  
  screen.timeout(5000)
  curses.curs_set(0) # Invisible cursor
  while not curses.isendwin():
    if settings['helptoggle']:
      display_help(screen)
    else:
      display(screen)


    char = screen.getch()
    
    if char == ord('q'): # quit
      return
    elif char == ord('z'): # increase compact
      settings['compact'] = min(settings['compact']+1, maxcompact)
      continue
    elif char == ord('Z'): # decrease compact
      settings['compact'] = max(settings['compact']-1, mincompact)
      continue
    elif char == ord('c'): # clear screen
      screen.clear()
      continue
    elif (char == ord('?')) or (char == ord('h')): #helpmenu
      settings['helptoggle'] ^= True
      continue
    else:
      continue
  
if __name__ == '__main__':
  #
  # Parse arguments and call the main subroutine of the program
  #
  try:

    parser = argparse.ArgumentParser(
      description=os.path.basename(sys.argv[0]))

    parser.add_argument('--quiet', '-q', help='Skip notice when starting', dest='skipnotice', action='store_true')
    
    args = parser.parse_args()

    # By default, display licensing tidbit
    if not args.skipnotice:
      print("{0} version {1}, Copyright (C) {2} {3}".format(__progname__, __version__, __year__, __author__))
      print(("{0} comes with ABSOLUTELY NO WARRANTY. This is free\n"+
        "software, and you are welcome to redistribute it under\n"+
        "certain conditions; press 'L' while active for details.").format(__progname__))

      raw_input("Press <Enter> to continue ")

    curses.wrapper(main)

    sys.exit(0)

  except KeyboardInterrupt as e:
    sys.exit(1)
    raise e ## Should never get here
  
  except SystemExit as e:
    raise e
  
  except Exception as e:
    print(str(e))
    traceback.print_exc()
    sys.exit(1)

