""" schema classes """
from app import app
from app.models import Deploy
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)


class DeploySchema(ma.ModelSchema):
    class Meta:
        model = Deploy
        fields = (
            "id",
            "host",
            "username",
            "password",
            "dbnames",
            "tool",
            "status",
            "isActive",
            "expiry",
            "created_at"
        )  # fields to expose
deployment_schema = DeploySchema()
deployments_schema = DeploySchema(many=True)