# SPDX-License-Identifier: MIT

import os
import os.path
import re

import pytest

import build.__main__


_SDIST = re.compile('.*.tar.gz')
_WHEEL = re.compile('.*.whl')


@pytest.mark.parametrize(
    ('project'),
    [
        'python-build',
        'pip',
        'dateutil',
        'Solaar',
    ]
)
@pytest.mark.parametrize(
    ('args'),
    [
        [],
        ['-x', '--no-isolation'],
    ]
)
def test_build(tmpdir, integration_path, project, args):
    os.environ['SETUPTOOLS_SCM_PRETEND_VERSION'] = 'dummy'  # for the projects that use setuptools_scm

    if project == 'python-build':  # windows does not support symlinks
        path = os.path.abspath(os.path.join(__file__, '..', '..'))
    else:
        path = os.path.join(integration_path, project)

    build.__main__.main([path, '-o', tmpdir] + args)

    assert filter(_SDIST.match, os.listdir(tmpdir))
    assert filter(_WHEEL.match, os.listdir(tmpdir))


def test_isolation(tmpdir, test_flit_path, mocker):
    try:
        import flit_core  # noqa: F401
    except:  # noqa: E722
        pass
    else:
        pytest.xfail('flit_core is available')

    mocker.patch('build.__main__._error')

    build.__main__.main([test_flit_path, '-o', tmpdir, '--no-isolation'])
    build.__main__._error.assert_called_with("Backend 'flit_core.buildapi' is not available")
