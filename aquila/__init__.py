from flask import Flask

from aquila.endpoints.healthz import bp as healthz_bp
from aquila.endpoints.rewards import bp as rewards_bp
from aquila.settings import PROJECT_NAME


def create_app() -> Flask:
    app = Flask(PROJECT_NAME)
    app.register_blueprint(rewards_bp)
    app.register_blueprint(healthz_bp)

    return app


# TODO: tests
# TODO: update bases/cosmos/polaris/core/lsp.yaml for polaris new endpoint
