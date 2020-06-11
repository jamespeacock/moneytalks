from collections import defaultdict
from json import JSONDecodeError
import logging
import math
import os

from crpapi import CRP
import pandas as pd

NAN = float('nan')

crp = CRP(os.environ.get("API_KEY"))

_CID = 2
_CRPNAME = 3
_PARTY = 4
_DIST_ID = 5
_CAND_ID = 6

CID = "cid"
PARTY = "party"
DISTRICT = "district"
FEC_ID = "fec_id"

CRP_IDS = 'CRP_IDs.xls'
CRP_CATS = 'CRP_Categories.txt'
CRP_COMMS = 'CRP_CongCmtes.txt'

ATTRS = '@attributes'

# attributes
OFFICE = 'office'  # e.g. CA12
GENDER = 'gender'
FIRST_ELEC = 'first_elected'
NAME = 'firstlast'
WEBFORM = 'webform'
PHONE = 'phone'
BDAY = 'birthdate'
TWTR = 'twitter_id'
YT = 'youtube_url'
FB = 'facebook_id'
CONGRESS_OFFICE = 'congress_office'
COMMENTS = 'comments'


def build_candidate_map():
    crp_ids_df = pd.read_excel(CRP_IDS)
    _map = {}
    cont = False
    for row in crp_ids_df.itertuples():
        if cont or row[0] > 12:
            cont = True
            info = {CID: row[_CID], PARTY: row[_PARTY],
                                  DISTRICT: row[_DIST_ID], FEC_ID: row[_CAND_ID]}

            # Add additional attrs from API if desired...
            # ...
            _map[row[_CRPNAME]] = info

    return _map


cand_map = build_candidate_map()  # map of formatted name to CID


def cand(name):
    return cand_map[name]


def cid(name):
    return cand_map[name][CID]


def _get_attrs(obj, attrs):
    att = {}
    for a in attrs:
        att[a] = obj[a] if a in obj else ""
    return att


def get_candidate_crp(name, attrs=('office',)):
    _cid = cid(name)
    try:
        _cand = crp.candidates.get(_cid)
    except JSONDecodeError:
        logging.log(logging.ERROR, "API KEY NOT FOUND")
        _cand = None
    return _get_attrs(_cand[ATTRS], attrs) if _cand else {}


def build_state_map():
    state_map = defaultdict(list)
    for name, c in cand_map.items():
        info = get_candidate_crp(name)
        if OFFICE in info:
            state_map[info[OFFICE][:2]].append(c[CID])

    return state_map


# state_map = build_state_map()
# def cands_in_state(state):
#     return state_map[state] if state in state_map else {}


def get_contributions(cid, year='2016', attrs=('org_name',)):
    contribs = crp.candidates.contrib(cid, year)
    return [_get_attrs(c[ATTRS], attrs) for c in contribs]

