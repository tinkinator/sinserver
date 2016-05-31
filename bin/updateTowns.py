#!/usr/bin/env python

import datetime, StringIO, zlib, os, urllib2, time, re
import xml.etree.ElementTree as ET
# from apps.towninfo.models import Town, Town_history, Player
import argparse
import django
from django.core.exceptions import ObjectDoesNotExist



def download_xml(url):
    '''
    Download XML and save it as a file
    '''
    print "Opening url %s..." %(url)
    request = urllib2.Request(url)
    request.add_header('Accept-encoding', 'gzip,deflate')
    response = urllib2.urlopen(request)
    READ_BLOCK_SIZE = 1024*8

    #set filename
    date = str(datetime.datetime.utcnow())[0:-16]
    filename = "datafile_towns_" + date + ".xml"
    outfile = open(os.path.join(path, filename), 'w')

    #decompress a gzipped stream of data
    d = zlib.decompressobj(16+zlib.MAX_WBITS)
    while True:
        data = response.read(READ_BLOCK_SIZE)
        if not data: break
        data = d.decompress(data)
        outfile.write(data)
    outfile.close()
    return filename
    
def get_town_variables(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    towns = root.findall(".//*townname/../..")
    print "parsing towns file..."
    cur_town = {}
    cur_town['data_gen_date'] = root.find('server').find('datagenerationdatetime').text[0:10]
    for town in towns:
        cur_town['townid'] = int(town.find('towndata').find('townname').get('id'))
        cur_town['player_id'] = int(town.find('player').find('playername').get('id'))
        alliance = town.find('player').find('playeralliance')
        cur_town['town_name']= town.find('towndata').find('townname').text
        cur_town['player_name'] = town.find('player').find('playername').text
        cur_town['founded_on'] = town.find('towndata').find('foundeddatetime').text
        if alliance is not None:
            cur_town['alliance'] = town.find('player').find('playeralliance').find('allianceticker').text
        else:
            cur_town['alliance'] = ''
        cur_town['mapx'] = int(town.find('location').find('mapx').text)
        cur_town['mapy'] = int(town.find('location').find('mapy').text)
        towns_hash[cur_town['townid']] = cur_town['town_name']
        save_inDB(cur_town)
        print "Processed town in db %s" %(cur_town['townid'])
    check_disappeared_towns()

def save_inDB(thetown):
    DFORMAT1 = "%Y-%m-%d"
    DFORMAT2 = "%Y-%m-%dT%H:%M:%S.%f"
    DFORMAT3 = "%Y-%m-%dT%H:%M:%S"
    changeDate = datetime.datetime.fromtimestamp(time.mktime(time.strptime(thetown['data_gen_date'], DFORMAT1)))
    try:
        town = Town.objects.get(townid=thetown['townid'])
    # if town doesn't exist save new town and new player
    except ObjectDoesNotExist:
        try:
            player = Player.objects.get(playerid = thetown['player_id'])
        except ObjectDoesNotExist:
            player = Player(
                playerid = thetown['player_id'],
                name = thetown['player_name'],
                player_alliance = thetown['alliance']
            )
            player.save()
        town = player.town_set.create(
            townid = thetown['townid'],
            name = thetown['town_name'],
            mapX = thetown['mapx'],
            mapY = thetown['mapy'],
            player = player
        )
        if len(thetown['founded_on']) == 19:
            format = DFORMAT3
        else:
            format = DFORMAT2
        newhist = town.town_history_set.create(
            town = town,
            founded_on = datetime.datetime.fromtimestamp(time.mktime(time.strptime(thetown['founded_on'], format))),
            change_type = "new", 
            change_date = changeDate
        )
    # if town exists check if anything has changed
    if town.name != thetown['town_name']:
       newhist = town.town_history_set.create(
           town = town,
           change_type = "renamed",
           change_date = changeDate,
           previous_status = town.name,
           current_status = thetown['town_name']
       )
       town.name = thetown['town_name']
       town.save() 
        
    if town.mapX != thetown['mapx'] or town.mapY != thetown['mapy']:
        newhist = town.town_history_set.create(
            town = town,
            change_type = "relocated",
            change_date = changeDate,
            previous_status = str(town.mapX) + " ; " + str(town.mapY),
            current_status = str(thetown['mapx']) + " ; " + str(thetown['mapy'])  
        )
        town.mapX = thetown['mapx']
        town.mapY = thetown['mapy']
        town.save()
        
    if town.player.player_alliance != thetown['alliance']:
        player = Player.objects.get(playerid = thetown['player_id'])
        newhist = town.town_history_set.create(
            town = town,
            change_type = "changed alliance",
            changed_datet = changeDate,
            previous_status = player.player_alliance,
            current_status = thetown['alliance']
        )
        
        playerhist = player.player_history_set.create(
            player = player,
            changed_alliance_at = changeDate,
            prev_status = player.player_alliance,
            curr_status = thetown['alliance'] 
        )
        player.player_alliance = thetown.alliance
        player.save()

    if check_abandoned(town.player.name):
        newhist = town.town_history_set.create(
            town = town,
            change_type = "abandoned",
            change_date = changeDate,
            previous_status = "active",
            current_status = "abandoned"    
        )
        playerhist = town.player.player_history_set.create(
            player = town.player,
            abandoned_at = changeDate,
            prev_status = "active",
            current_status = "abandoned"
        )
        
    if town.player.name != thetown['player_name']:
       player = Player.objects.get(playerid = thetown['player_id'])
       playerhist = player.player_history_set.create(
           player = player,
           change_type = "player name",
           change_date = changeDate,
           prev_status = player.name,
           curr_status = thetown['player_name']
       )
       player.name = thetown['player_name']
       player.save()

def check_abandoned(player_name):
    return re.search('(\(Abandoned\))+', player_name)
 
def check_disappeared_towns():
    towns = Town.objects.values('townid').values()[0]
    for town in towns:
        print town
        if town not in towns_hash:
            print "%s not in towns hash!" % (town)
            townhist = Town_history.objects.all().filter(town=town).order_by('-change_date')[0]
            if townhist.change_type != "disappeared":
                newhist = town.town_history_set.create(
                    town = town,
                    change_type = "disappeared",
                    change_date = datetime.datetime.now()
                )
            else:
                # if more than 316 hours passed, the town has been destroyed, captured, or otherwise disappeared
                timediff = datetime.datetime.now() - townhist.change_date
                if divmod(timediff.total_seconds(), 3600) > 316:
                      newhist = town.town_history_set.create(
                          town = town,
                          change_type = "destroyed",
                          change_date = datetime.datetime.now()
                      )

def main():
    parser = argparse.ArgumentParser(description='Download file from url or from file')
    parser.add_argument('option', action='store', help="enter 'file' or 'url'")
    parser.add_argument('date', action='store', help="enter date of the xml file in the 'YYYY-MM-DD' format")
    args = parser.parse_args()
    if args.option == 'file':
        pathtofile = os.path.expanduser('~') + '/code/tinkdar/xml/'
        filename = os.path.join(pathtofile, 'datafile_towns_{filedate}.xml'.format (filedate=args.date))
        print filename
        get_town_variables(filename)
    elif args.option == 'url':
        filename = download_xml("http://data-root.illyriad.co.uk/datafile_towns.xml")

if __name__ == '__main__':
    if __package__ is None:
        print "foo"
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
        from sinserver import setup
        setup()
        from apps.towninfo.models import Town, Town_history, Player
        
        # from sinserver.settings import BASE_DIR
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR, "data/townxmls/")
        towns_hash = {}
        main()
    else:
        print "bar"
        from ..apps.towninfo.models import Town, Town_history, Player
        from ..sinserver import settings, setup
        setup()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR, "data/townxmls/")
        towns_hash = {}
