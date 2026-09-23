from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from monitoring.demo_data.seed import DemoDataError, seed_demo_data


class Command(BaseCommand):
    help = "Create deterministic workshop demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing DEMO-* stations before seeding.",
        )
        parser.add_argument(
            "--large",
            action="store_true",
            help="Create about 1,000 measurements per sensor.",
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo_data is available only when DEBUG=True.")

        try:
            result = seed_demo_data(
                reset=options["reset"],
                large=options["large"],
            )
        except DemoDataError as error:
            raise CommandError(str(error)) from error

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded demo data: "
                f"{result.users} users, {result.stations} stations, "
                f"{result.sensors} sensors, {result.measurements} measurements."
            )
        )