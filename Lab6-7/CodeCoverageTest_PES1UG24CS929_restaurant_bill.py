import pytest
from restaurant_bill import bill_total, split_bill, table_wait


# --- bill_total ---

def test_dine_in_no_happy_hour():
    assert bill_total("dine_in", 1000, 2, False) == 1155

def test_dine_in_happy_hour():
    # is_happy_hour True + dine_in → 20% discount applied
    assert bill_total("dine_in", 1000, 2, True) == 924

def test_takeaway_happy_hour_no_discount():
    # happy_hour True but section == takeaway → no discount
    assert bill_total("takeaway", 1000, 2, True) == 1050

def test_rooftop_no_happy_hour():
    assert bill_total("rooftop", 500, 2, False) == 603

def test_large_party_surcharge():
    # guests >= 8 → extra 200 added to service
    assert bill_total("dine_in", 1000, 8, False) == 1365

def test_invalid_section():
    with pytest.raises(ValueError):
        bill_total("bar", 100, 2, False)

def test_negative_food_total():
    with pytest.raises(ValueError):
        bill_total("dine_in", -1, 2, False)

def test_zero_guests():
    with pytest.raises(ValueError):
        bill_total("dine_in", 100, 0, False)


# --- split_bill ---

def test_even_split():
    assert split_bill(1000, 4, 10) == 275

def test_uneven_split_rounds_up():
    # 101 // 4 = 25 remainder 1 → returns 26
    assert split_bill(101, 4, 0) == 26

def test_invalid_people():
    with pytest.raises(ValueError):
        split_bill(100, 0, 10)

def test_negative_tip():
    with pytest.raises(ValueError):
        split_bill(100, 2, -5)


# --- table_wait ---

def test_party_too_large():
    assert table_wait(13, 5, False) == "call ahead"

def test_has_reservation_seated():
    assert table_wait(4, 0, True) == "seat now"

def test_no_free_tables_waitlist():
    assert table_wait(4, 0, False) == "waitlist"

def test_large_party_insufficient_tables():
    # party_size > 6 and free_tables < 2
    assert table_wait(7, 1, False) == "waitlist"

def test_small_party_free_table():
    assert table_wait(4, 3, False) == "seat now"
