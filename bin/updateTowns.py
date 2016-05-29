import datetime, StringIO, zlib, os, urllib2, time, re
import xml.etree.ElementTree as ET
from ..apps.towninfo.models import Town, Town_history, Player
from ..sinserver.settings import BASE_DIR
import argparse
from django.core.exceptions import ObjectDoesNotExist

path = os.path.join(BASE_DIR, "data/townxmls/")
towns_hash = {}

def download_xml(url):
    '''
    Download XML and save it as a file
    '''
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
    tree = ET.parse(xml_file)
    root = tree.getroot()
    towns = root.findall(".//*townname/../..")
    cur_town = {}
    for town in towns:
        cur_town.townid = int(town.find('towndata').find('townname').get('id'))
        cur_town.player_id = int(town.find('player').find('playername').get('id'))
        cur_town.alliance = town.find('player').find('playeralliance')
        cur_town.town_name = town.find('towndata').find('townname').text
        cur_town.player_name = town.find('player').find('playername').text
        cur_town.founded_on = town.find('towndata').find('foundeddatetime').text
        if alliance is not None:
            cur_town.alliance = town.find('player').find('playeralliance').find('allianceticker').text
        else:
            cur_town.alliance = ''
        cur_town.mapx = int(town.find('location').find('mapx').text)
        cur_town.mapy = int(town.find('location').find('mapy').text)
        cur_town.data_gen_date = root.find('server').find('datagenerationdatetime').text[0:10]
        towns_hash[cur_town.townid] = cur_town.town_name
        save_inDB(cur_town)

def save_inDB(thetown):
    DFORMAT = "%Y-%m-%dT%H:%M:%S.%f"
    changeDate = time.strptime(thetown.data_gen_date, DFORMAT)
    try:
        town = Town.objects.get(townid=thetown.townid)
    # if town doesn't exist save new town and new player
    except ObjectDoesNotExist:
        try:
            player = Player.objects.get(playerid = thetown.player_id)
        except ObjectDoesNotExist:
            player = Player(
                playerid = thetown.player_id,
                name = thetown.player_name,
                player_alliance = thetown.alliance
            )
            player.save()
        player.town_set.create(
            townid = thetown.townid,
            name = thetown.town_name,
            mapX = thetown.mapx,
            mapY = thetown.mapy,
            player = player
        )
        town.town_history_set.create(
            town = town,
            founded_on = time.strptime(thetown.founded_on, DFORMAT),
            registered_at = changeDate
        )
    # if town exists check if anything has changed
    if town.name != thetown.town_name:
       town.history_set.create(
           town = town,
           renamed_at = changeDate,
           previous_status = town.name,
           current_status = thetown.town_name
       )
       town.name = thetown.town_name
       town.save() 
        
    if town.mapX != thetown.mapx || town.mapY != thetown.mapy:
        town.history_set.create(
            town = town,
            relocated_at = changeDate,
            previous_status = str(town.mapX) + " ; " + str(town.mapY),
            current_status = str(thetown.mapx) + " ; " + str(thetown.mapy)  
            
        )
        town.mapX = thetown.mapx
        town.mapY = thetown.mapy
        town.save()
        
    if town.player.player_alliance != thetown.alliance:
        town.history_set.create(
            town = town,
            changed_alliance_at = changeDate,
            
        )
        
    if checkAbandoned(town.player_name):
        
def checkAbandoned(player_name):
    return re.search('(\(Abandoned\))+', player_name) 
       


        