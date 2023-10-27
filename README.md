# docxtmpl

A simple service written in Python that takes a docx file, renders it using [doxtpl](https://docxtpl.readthedocs.io) and then converts it to PDF using [LibreOffice](https://libreoffice.org).

## Running the Docker Container

The project is packaged as a Docker container. Run it as

```shell
docker run -e AUTH_TOKEN=<token> ghcr.io/lmr-hh/docxtmpl
```

The image can be configured with the following environment variables

| Variable          | Default   | Description                                                  |
| ----------------- | --------- | ------------------------------------------------------------ |
| `AUTH_TOKEN`      | *Not set* | If you set `AUTH_TOKEN` to a non-empty string, each request must provide the value as `Bearer` token, otherwise a 401 or 403 error will be returned. If you leave this unset, every request is accepted. |
| `AUTH_TOKEN_FILE` | *Not set* | If you want to use Docker secrets you can set `AUTH_TOKEN_FILE` instead of `AUTH_TOKEN`. An explicit `AUTH_TOKEN` takes precedence over this field |

The docker container contains some commonly used fonts.

## Using the Service

The `docxtmpl` service accepts Multipart `POST` requests containing exactly one `template` file and a `data` field containing a JSON object with the templating context. A request might look like this:

```http
POST / HTTP/1.1
Accept: application/pdf
Authorization: Bearer <token>
Content-Type: multipart/form-data; boundary=AaB03x--

--AaB03x--
Content-Disposition: form-data; name="template"; filename="some-filename.docx"
Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document

... template file contents
--AaB03x--
Content-Disposition: form-data; name="data"

{"some": "field", "another": 1234}
```

The response to a valid request is the raw PDF data. The `Content-Disposition` header might suggest a name for the PDF file.