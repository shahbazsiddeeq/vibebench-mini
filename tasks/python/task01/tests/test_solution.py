from src.solution import add
def test_add_basic(): assert add(1,2)==3
def test_add_zero(): assert add(0,0)==0
def test_add_negative(): assert add(-5,2)==-3
