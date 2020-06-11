from utils import get_candidate_crp, cand, cid, get_contributions, cands_in_state

PELOSI = 'Pelosi, Nancy'


def test_candidate_load():

    assert cid(PELOSI) == 'N00007360'
    assert cand(PELOSI) == {'cid': 'N00007360', 'party': 'D', 'district': 'CA12', 'fec_id': 'H8CA05035'}
    cand_info = get_candidate_crp(PELOSI)
    assert cand_info['firstlast'] == 'Nancy Pelosi'


def state_sort_map():
    ids_by_state = cands_in_state('OH')
    assert len(ids_by_state) == 0


def test_contribution_info():
    contribs = get_contributions(cid(PELOSI), '2016')
    assert contribs

### Tests for partial search