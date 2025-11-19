import os
from .library import Library
from .utils import normalize_title, scan_folder_for_posters

def test_db_create_and_crud(tmp_path):
    db_file = tmp_path / 'cine_test.db'
    lib = Library(str(db_file))
    mid = lib.add_movie('Test Movie', 2000, ['Drama'], ['test'], 'synopsis', None)
    assert mid > 0
    m = lib.get_movie(mid)
    assert m.title == 'Test Movie'
    lib.update_movie(mid, title='New Title')
    m2 = lib.get_movie(mid)
    assert m2.title == 'New Title'
    lib.delete_movie(mid)
    assert lib.get_movie(mid) is None
    lib.close()

def test_utils(tmp_path):
    assert normalize_title('  hello  WORLD  ') == 'Hello World'
    d = tmp_path / 'images'
    sub = d / 'sub'
    sub.mkdir(parents=True)
    f = d / 'a.jpg'
    f.write_text('x')
    f2 = sub / 'b.png'
    f2.write_text('y')
    found = scan_folder_for_posters(str(d))
    assert len(found) == 2
