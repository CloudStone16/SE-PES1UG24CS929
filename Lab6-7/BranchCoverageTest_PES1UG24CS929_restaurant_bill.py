import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# --- bill_total branches ---

# Branch: section not in SERVICE_CHARGE → True
def test_invalid_section_raises():
    with pytest.raises(ValueError):
        bill_total("bar", 100, 2, False)

# Branch: section not in SERVICE_CHARGE → False (valid section continues)
def test_valid_section_dine_in():
    assert bill_total("dine_in", 1000, 2, False) == 1155

# Branch: food_total < 0 → True
def test_negative_food_total_raises():
    with pytest.raises(ValueError):
        bill_total("dine_in", -1, 2, False)

# Branch: guests < 1 → True
def test_zero_guests_raises():
    with pytest.raises(ValueError):
        bill_total("dine_in", 100, 0, False)

# Branch: is_happy_hour and section != "takeaway" → True
def test_happy_hour_dine_in_discount():
    # food_total 1000 * 80//100 = 800; service 80; total 880; +5% = 924
    assert bill_total("dine_in", 1000, 2, True) == 924

# Branch: is_happy_hour and section != "takeaway" → False (no happy hour)
def test_no_happy_hour_no_discount():
    assert bill_total("rooftop", 500, 2, False) == 603

# Branch: is_happy_hour True but section == "takeaway" → condition False
def test_takeaway_happy_hour_skips_discount():
    assert bill_total("takeaway", 1000, 2, True) == 1050

# Branch: guests >= 8 → True
def test_large_party_extra_service():
    # service = 100 + 200 = 300; total = 1300; +5% = 1365
    assert bill_total("dine_in", 1000, 8, False) == 1365

# Branch: guests >= 8 → False
def test_small_party_no_extra_service():
    assert bill_total("dine_in", 1000, 7, False) == 1155


# --- split_bill branches ---

# Branch: people < 1 → True
def test_invalid_people_raises():
    with pytest.raises(ValueError):
        split_bill(100, 0, 10)

# Branch: tip_percent < 0 → True
def test_negative_tip_raises():
    with pytest.raises(ValueError):
        split_bill(100, 2, -1)

# Branch: grand_total % people != 0 → True (rounds up)
def test_uneven_split_rounds_up():
    assert split_bill(101, 4, 0) == 26

# Branch: grand_total % people == 0 → False (exact)
def test_even_split_no_rounding():
    assert split_bill(1000, 4, 10) == 275

# Branch: people >= 1 and tip >= 0 (normal path)
def test_split_with_tip():
    assert split_bill(200, 5, 20) == 48


# --- table_wait branches ---

# Branch: party_size > 12 → True
def test_oversized_party_call_ahead():
    assert table_wait(13, 5, False) == "call ahead"

# Branch: party_size > 12 → False, has_reservation → True
def test_reservation_seat_now():
    assert table_wait(4, 0, True) == "seat now"

# Branch: no reservation, free_tables == 0 → True
def test_no_tables_waitlist():
    assert table_wait(4, 0, False) == "waitlist"

# Branch: no reservation, free_tables > 0, party_size > 6 and free_tables < 2 → True
def test_large_party_one_table_waitlist():
    assert table_wait(7, 1, False) == "waitlist"

# Branch: no reservation, free_tables > 0, party_size > 6 and free_tables >= 2 → False (seat now)
def test_large_party_enough_tables_seat_now():
    assert table_wait(7, 2, False) == "seat now"

# Branch: no reservation, free_tables > 0, party_size <= 6 (seat now via else)
def test_small_party_seat_now():
    assert table_wait(4, 1, False) == "seat now"
