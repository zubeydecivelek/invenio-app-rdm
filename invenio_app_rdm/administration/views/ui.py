# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2024 CERN.
#
# Invenio App RDM is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Administration ui views module."""

from flask import Blueprint, Response, abort, g, jsonify
from flask_login import login_required
from invenio_records_resources.services.errors import PermissionDeniedError
from invenio_users_resources.proxies import current_user_resources


@login_required
def export_user(user_id):
    """Export user data as ZIP file."""
    try:
        # Get the users service
        users_service = current_user_resources.users_service
        
        # Get the current identity
        identity = g.identity
        
        # Read the user
        user = users_service.read(identity, user_id)
        
        # Serialize user data
        user_data = user.to_dict()
        
        # TODO: Implement zip file creation logic here
        # Create zip file with user data
        # zip_data = create_user_export_zip(user_data)
        
        # Placeholder: return JSON for now (will be replaced with zip)
        zip_data = jsonify(user_data).get_data(as_text=False)
        
        # Return as ZIP with download headers
        response = Response(
            zip_data,
            mimetype="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename=user_{user_id}.zip"
            }
        )
        
        return response
    except PermissionDeniedError:
        abort(403)
    except Exception:
        abort(404)


def create_ui_blueprint(app):
    """Register blueprint routes on app."""
    blueprint = Blueprint(
        "invenio_app_rdm_administration",
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    
    # Register export route
    blueprint.add_url_rule(
        "/export/<user_id>",
        "export_user",
        export_user,
        methods=["GET"],
    )

    return blueprint
