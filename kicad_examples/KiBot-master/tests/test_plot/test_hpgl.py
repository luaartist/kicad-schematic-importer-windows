"""
Tests of HPGL format.

For debug information use:
pytest-3 --log-cli-level debug
"""
from . import context
PS_DIR = 'HPGL'


def test_hpgl(test_dir):
    prj = 'simple_2layer'
    ctx = context.TestContext(test_dir, prj, 'hpgl', PS_DIR)
    ctx.run()
    ctx.expect_out_file(ctx.get_gerber_filename('F_Cu', '.plt'))
    ctx.expect_out_file(ctx.get_gerber_filename('B_Silks', '.plt'))
    ctx.dont_expect_out_file(ctx.get_gerber_job_filename())
    ctx.clean_up()


def test_hpgl_auto(test_dir):
    prj = 'simple_2layer'
    ctx = context.TestContext(test_dir, prj, 'hpgl_auto', PS_DIR)
    ctx.run()
    ctx.expect_out_file(ctx.get_gerber_filename('F_Cu', '.plt'))
    ctx.expect_out_file(ctx.get_gerber_filename('B_Silks', '.plt'))
    ctx.dont_expect_out_file(ctx.get_gerber_job_filename())
    ctx.search_err(r'Only ASCII chars are allowed for layer suffixes')
    ctx.clean_up()
