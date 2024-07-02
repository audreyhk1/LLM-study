from old_code.old import find_choices

def test_find_choices():
    assert find_choices("\n(A) alkdj f;lksdj f\n(A) \n(A) \n(A) ", ["1", "2", "3"]) == "3"