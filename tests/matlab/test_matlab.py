from neurolib import matlab


def test_str_command():
    (retcode, _, _) = matlab.run('disp([1 2 3])')
    assert retcode == 0


def test_list_command():
    (retcode, stderr, _) = matlab.run(["disp('hello')", "disp('world')"])
    assert retcode == 0
    assert stderr.split('\n')[-3:] == ['hello', 'world', '']
