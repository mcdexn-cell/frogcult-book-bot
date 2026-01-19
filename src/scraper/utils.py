"""
Provide utils for parser.
"""

from typing import Any
import re

from playwright.async_api import (
    Locator,
    Page,
)

from src.enums.scraper import ParseMode
from src.structures.scraper import ParserFieldConfig


async def parse_field(field_config: ParserFieldConfig, locator: Locator) -> str | None:
    """
    Parse a single field from page locator.

    Args:
        field_config: field configuration.
        locator: Locator to parse.\

    Returns:
        parsed and normalized field.
    """
    if field_config.attribute is None:
        raw_field = await locator.text_content()

    else:
        raw_field = await locator.get_attribute(name=field_config.attribute)

    field_value = str(raw_field).strip()

    if field_config.regex is not None:
        try:
            field_value = re.findall(field_config.regex, field_value)[field_config.regex_index]

        except IndexError:
            return None

    return field_value


async def parse_config(
        config: dict[str, ParserFieldConfig],
        target: Locator | Page,
) -> dict[str, Any]:
    """
    Parse data from locator with provided config.

    Args:
        config: parsing config.
        target: target to parse.

    Returns:
        parsed data.
    """
    result = {}

    for field_name, field_config in config.items():
        all_selectors = await target.locator(field_config.selector).all()
        if len(all_selectors) == 0:
            continue

        if field_config.mode == ParseMode.ALL:
            field_value = [
                await parse_field(field_config=field_config, locator=locator)
                for locator in all_selectors
            ]
        else:
            field_value = await parse_field(field_config=field_config, locator=all_selectors[0])

        result[field_name] = field_value

    return result
