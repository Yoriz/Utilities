'''
Created on 14 Feb 2012

@author: Dave Wilson
'''

from math import ceil
from collections import namedtuple

Page = namedtuple('Page', 'pageNo noPages noRecords recordsStart '
                         'recordsEnd details offset limit bottom top')


def validatePageNo(pageNo, noPages):
    try:
        pageNo = int(pageNo)
    except (TypeError, ValueError):
        return 1
    if pageNo < 1:
        return 1
    elif pageNo > noPages:
        return noPages

    return pageNo


def calcNoPages(noRecords, perPage, orphans):
    if not noRecords:
        return 1
    hits = max(1, noRecords - orphans)
    return int(ceil(hits / float(perPage)))


def pageDetails(pageNo, noPages, noRecords, recordsStart, recordsEnd):
    if not noRecords:
        return 'No Records'
    elif noPages == 1:
        pages = 'Page 1'
    else:
        pages = 'Page {} of {}'.format(pageNo, noPages)

    if noRecords == 1:
        records = '1 Record'
    else:
        records = 'Records {} to {}'.format(recordsStart, recordsEnd)

    if noPages > 1:
        records = '{} of {} Records'.format(records, noRecords)

    return '{} - {}'.format(pages, records)


def pagination(pageNo, noRecords, perPage=1000, orphans=0):
    noPages = calcNoPages(noRecords, perPage, orphans)
    pageNo = validatePageNo(pageNo, noPages)
    recordsStart = perPage * (pageNo - 1) + 1 if noRecords > 1 else 1
    recordsEnd = pageNo * perPage if pageNo != noPages else noRecords
    offset = bottom = recordsStart - 1
    limit = recordsEnd - offset
    top = bottom + limit
    details = pageDetails(pageNo, noPages, noRecords, recordsStart, recordsEnd)
    return Page(pageNo, noPages, noRecords, recordsStart, recordsEnd, details,
                       offset, limit, bottom, top)

if __name__ == '__main__':
    print pagination(2, 3005)
    print pagination(4, 3005)
