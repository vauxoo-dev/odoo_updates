import click
from unittest import TestCase
from click.testing import CliRunner
from odoo_updates import utils, odoo_updates

class TestUpdatesv(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()

    def test_01_cli(self):
        @click.group()
        @click.option('--original', '-o', required=True)
        @click.option('--updated', '-u', required=True)
        @click.option('--screen', '-s', is_flag=True, default=False)
        @click.option('--queue', '-q', envvar='AWS_BRANCH_QUEUE', default=False)
        @click.option('--customer', '-c', envvar='CUSTOMER', required=True)
        @click.pass_context
        def cli(ctx, original, updated, screen, queue, customer):
            ctx.obj.update({'original': original})
            ctx.obj['updated'] = updated
            ctx.obj['screen'] = screen
            ctx.obj['queue'] = queue
            ctx.obj['customer'] = customer

        @cli.command()
        @click.pass_context
        def views(ctx):
            views_states = odoo_updates.get_views_diff(ctx.obj['original'], ctx.obj['updated'])
            if ctx.obj['screen']:
                odoo_updates.diff_to_screen(views_states, 'views')
            else:
                message = utils.jsonify(views_states, 'views', ctx.obj['customer'])
                utils.send_message(message, ctx.obj['queue'])

        res = self.runner.invoke(cli, ['origin', 'updated', '-s', 'queue', 'customer', 'views'])
