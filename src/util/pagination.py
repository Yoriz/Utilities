'''
Created on 14 Feb 2012

@author: Dave Wilson
'''

import math
import collections


class PageObj(collections.namedtuple('PageObj', ('page_no', 'num_records',
            'num_pages', 'page_details', 'bottom', 'top', 'limit',
            'offset'))):
    '''Represents a paginated page'''
    __slots__ = ()

    @property
    def slice(self):
        '''Returns a slice object using bottom and top values'''
        return slice(self.bottom, self.top)

    @property
    def has_next(self):
        '''Return True if the current page_no has a next page'''
        return self.page_no < self.num_pages

    @property
    def has_previous(self):
        '''Return True if the current page_no has a previous page'''
        return self.page_no > 1

    @property
    def previous_page_no(self):
        '''Returns the page no of the previous page'''
        return max(1, self.page_no - 1)

    @property
    def next_page_no(self):
        '''Returns the page no of the next page'''
        return min(self.num_pages, self.page_no + 1)

    @property
    def last_page_no(self):
        '''Returns the page_no of the last page'''
        return self.num_pages


def calc_no_pages(num_records, orphans, per_page):
    '''Calculates how many pages of records there are'''
    hits = max(1, num_records - orphans)
    return int(math.ceil(hits / float(per_page)))


def validate_page_no(page_no, num_pages):
    '''Validates the page number to stay in range of the number of pages'''
    return max(1, min(page_no, num_pages))


def calc_records_start(num_records, per_page, page_no):
    '''Calculates the row of the first record of the current page'''
    records_start = 0
    if num_records > 1:
        records_start = per_page * (page_no - 1) + 1
    return records_start


def calc_records_end(num_records, page_no, num_pages, per_page):
    '''Calculates the row of the last record of the current page'''
    records_end = num_records
    if page_no != num_pages:
        records_end = page_no * per_page
    return records_end


def create_page_details(num_records, num_pages, page_no, records_start,
        records_end):
    '''Creates the page details string'''
    if not num_records:
        return 'No Records'

    elif num_pages == 1:
        pages = 'Page 1'
    else:
        pages = 'Page {} of {}'.format(page_no, num_pages)

    if num_records == 1:
        records = '1 Record'
    else:
        records = 'Records {} to {}'.format(records_start,
                                            records_end)

    if num_pages > 1:
        records = '{} of {} Records'.format(records, num_records)

    return '{} - {}'.format(pages, records)


def calc_offset(records_start):
    '''Calculates the current page database offset'''
    return records_start - 1


def calc_limit(records_end, offset):
    '''Calculates the current page database limit'''
    return records_end - offset


def calc_top(bottom, limit):
    '''Calculates the top split value of the current page'''
    return bottom + limit


def make_pageobj(page_no=1, num_records=0, per_page=1000, orphans=0):
    '''Creates a paginated page obj'''
    num_pages = calc_no_pages(num_records, orphans, per_page)
    page_no = validate_page_no(page_no, num_pages)
    records_start = calc_records_start(num_records, per_page, page_no)
    records_end = calc_records_end(num_records, page_no, num_pages, per_page)
    page_details = create_page_details(num_records, num_pages, page_no,
        records_start, records_end)
    offset = bottom = calc_offset(records_start)
    limit = calc_limit(records_end, offset)
    top = calc_top(bottom, limit)

    return PageObj(page_no, num_records, num_pages, page_details,
        bottom, top, limit, offset)


if __name__ == '__main__':
    pagination_obj = make_pageobj(4, 3600)
    print pagination_obj.slice
    print pagination_obj.slice.stop - pagination_obj.slice.start
    print pagination_obj.offset, pagination_obj.limit
    print pagination_obj.page_details
