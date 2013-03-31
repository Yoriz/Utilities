'''
Created on 14 Feb 2012

@author: Dave Wilson
'''

from math import ceil
from collections import namedtuple

Page = namedtuple('Page', 'pageNo numPages numRecords recordsStart '
                         'recordsEnd details offset limit bottom top')


def validatePageNo(pageNo, numPages):
    try:
        pageNo = int(pageNo)
    except (TypeError, ValueError):
        return 1
    if pageNo < 1:
        return 1
    elif pageNo > numPages:
        return numPages

    return pageNo


def calcNoPages(numRecords, perPage, orphans):
    if not numRecords:
        return 1
    hits = max(1, numRecords - orphans)
    return int(ceil(hits / float(perPage)))


def pageDetails(pageNo, numPages, numRecords, recordsStart, recordsEnd):
    if not numRecords:
        return 'No Records'
    elif numPages == 1:
        pages = 'Page 1'
    else:
        pages = 'Page {} of {}'.format(pageNo, numPages)

    if numRecords == 1:
        records = '1 Record'
    else:
        records = 'Records {} to {}'.format(recordsStart, recordsEnd)

    if numPages > 1:
        records = '{} of {} Records'.format(records, numRecords)

    return '{} - {}'.format(pages, records)


def pagination(pageNo, numRecords, perPage=1000, orphans=0):
    numPages = calcNoPages(numRecords, perPage, orphans)
    pageNo = validatePageNo(pageNo, numPages)
    recordsStart = perPage * (pageNo - 1) + 1 if numRecords > 1 else 1
    recordsEnd = pageNo * perPage if pageNo != numPages else numRecords
    offset = bottom = recordsStart - 1
    limit = recordsEnd - offset
    top = bottom + limit
    details = pageDetails(pageNo, numPages, numRecords, recordsStart,
                          recordsEnd)
    return Page(pageNo, numPages, numRecords, recordsStart, recordsEnd,
                details, offset, limit, bottom, top)

if __name__ == '__main__':
    print pagination(2, 3005)
    print pagination(4, 3005)
