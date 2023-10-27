import io
import json
import subprocess
import tempfile
from os import path

import docxtpl
from flask import request, Response, send_file
from werkzeug.datastructures import WWWAuthenticate
from werkzeug.exceptions import BadRequest, Forbidden, InternalServerError, Unauthorized

from .app import app, auth_token


@app.post('/')
def do_template() -> Response:
    """HTTP endpoint, rendering docx to a templated PDF."""

    app.logger.info("Received conversion request")
    context = parse_request()
    try:
        template_filename = path.basename(request.files["template"].filename or "file.docx")
    except KeyError:
        raise BadRequest("no template provided")

    app.logger.info("Rendering docx template")
    template = docxtpl.DocxTemplate(
        io.BytesIO(request.files["template"].stream.read()))
    template.render(context, autoescape=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        app.logger.info(f"Saving rendered docx file to {tmpdir}")
        filename = path.join(tmpdir, f"file.docx")
        template.save(filename)
        app.logger.info("Converting docx template to PDF")
        # See https://help.libreoffice.org/latest/en-US/text/shared/guide/pdf_params.html
        # for available parameters.
        process = subprocess.run([
            "soffice",
            "--headless",
            "--convert-to",
            'pdf:draw_pdf_Export:{"SelectPdfVersion":{"type":"long","value":"2"}}',
            "--outdir",
            tmpdir,
            filename
        ])
        if process.returncode != 0:
            app.logger.error("Conversion failed, aborting")
            raise InternalServerError("could not convert file")
        app.logger.info("Responding with PDF file")
        return send_file(
            path.join(tmpdir, "file.pdf"),
            mimetype="application/pdf",
            as_attachment=True,
            download_name=f"{template_filename}.pdf"
        )


def parse_request() -> dict:
    """
    Checks if the request is authenticated and contains a valid dataset for templating.
    :return: The templating context data.
    """

    if auth_token and request.authorization is None:
        app.logger.warning("Request not authorized, aborting")
        raise Unauthorized(www_authenticate=WWWAuthenticate(auth_type="bearer"))
    if auth_token and (
            request.authorization.type != "bearer"
            or request.authorization.token != auth_token
    ):
        app.logger.warning("Request credentials invalid, aborting")
        raise Forbidden()
    try:
        return json.loads(request.form.get("data", "{}"))
    except json.decoder.JSONDecodeError:
        raise BadRequest("invalid JSON data")
