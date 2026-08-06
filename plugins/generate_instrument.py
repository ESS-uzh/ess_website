from pelican import signals
from pelican.contents import Page


def generate_instrument_page(generator):

    metadata = {
        "title": "Instrument Booking",
        "slug": "instrument",
        "template": "instrument",
        "save_as": "instrument/index.html",
        "url": "instrument",
    }

    page = Page(
        content="",
        metadata=metadata,
        source_path="instrument.md",
        context=generator.context,
        settings=generator.settings,
    )

    generator.pages.append(page)


def register():
    signals.page_generator_finalized.connect(generate_instrument_page)