import logging

import requests

from flask import Response, abort, render_template, render_template_string

from aquila.blob_storage import template_loader
from aquila.metrics import reward_requests_total
from aquila.settings import POLARIS_BASE_URL

logger = logging.getLogger(__name__)


def raise_template_error_response(retailer_slug: str) -> None:
    error_template = template_loader.get_template(retailer_slug, "error")
    if error_template:
        resp = Response(render_template_string(error_template))
        reward_requests_total.labels(retailer_slug=retailer_slug, response_status=200, response_template="error").inc()
    else:
        resp = Response(render_template("default_error.html"))
        reward_requests_total.labels(
            retailer_slug=retailer_slug, response_status=200, response_template="default_error"
        ).inc()

    abort(resp)


def get_polaris_reward(retailer_slug: str, reward_id: str) -> dict:
    """
    expected response payload from polaris will be:
    ```json
    {
        "code": "Reward redeeming code",
        "expiry_date": "2022-05-18",
        "template_slug": "name of template to use"
        "pin": "Optional field"
    }
    """
    try:
        response = requests.get(f"{POLARIS_BASE_URL}/{retailer_slug}/reward/{reward_id}", timeout=(3.05, 10))
    except Exception:  # pylint: disable=broad-except
        logger.exception("Unable to reach polaris")
        raise_template_error_response(retailer_slug)

    if response.status_code != 200:
        logger.info(
            "Received a negative response from polaris. Info: status: %d, response: %s",
            response.status_code,
            response.text,
        )
        if response.status_code == 404:
            reward_requests_total.labels(
                retailer_slug=retailer_slug, response_status=404, response_template="N/A"
            ).inc()
            abort(404)

        raise_template_error_response(retailer_slug)

    return response.json()
