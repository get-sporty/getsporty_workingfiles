#!/usr/bin/python

#Uses code from http://boscoh.com/programming/reading-xml-serially.html

import re   #parsing xml with regex, teehee

points = {}

att = re.compile(r'>([\w\d\.\'\s]+)</SimpleData>$')
coords = re.compile(r'<\w+><\w+><\w+><\w+>([-\d,\.\s]+)</\w+></\w+></\w+>')

def average(gpspos):
    tot = len(gpspos)
    new = []
    for i in range(2):
        av = sum([x[i] for x in gpspos]) / tot
        new.append(av)
    return tuple(new)

with open('ACT_Blocks.kml') as f:
    data = {}
    parsing = False
    for line in f:
        try:
            if line.startswith('  <Placemark'):
                parsing = True
                data = {}
            elif parsing:
                if "DIVISION_NAME" in line:
                    data["name"] = att.search(line).group(1)
                elif "BLOCK_NUMBER" in line:
                    data["block"] = att.search(line).group(1)
                elif "SECTION_NUMBER" in line:
                    data["section"] = att.search(line).group(1)
                elif line.startswith('      <Polygon>'):
                    c = coords.search(line).group(1)
                    if ' ' in c:
                        c = c.split(' ')
                    else:
                        c = [c]
                    c = map(lambda a: (float(a.split(',')[0]), float(a.split(',')[1]) ), c)
                    data['coord'] = average(c)
                if line.startswith('  </Placemark>'):
                    parsing = False
                    try:
                        points[(data["name"], data["block"], data["section"])] = data['coord']
                        #print (data["name"], data["block"], data["section"], data['coord'])
                    except KeyError:
                        continue
        except Exception as e:
            print line
            print e
            break