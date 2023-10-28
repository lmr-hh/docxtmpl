# docxtmpl

A simple service written in Python that takes a docx file, renders it using [doxtpl](https://docxtpl.readthedocs.io) and then converts it to PDF using [LibreOffice](https://libreoffice.org).

## Running the Docker Container

The project is packaged as a Docker container. Run it as

```shell
docker run -e DOCXTMPL_API_KEY=<api-key> ghcr.io/lmr-hh/docxtmpl
```

The image can be configured with the following environment variables

| Variable                | Default   | Description                                                  |
| ----------------------- | --------- | ------------------------------------------------------------ |
| `DOCXTMPL_API_KEY`      | *Not set* | If you set `DOCXTMPL_API_KEY` to a non-empty string, each request must provide the value in a `Api-Key` header, otherwise a 401 or 403 error will be returned. If you leave this unset, every request is accepted.<br />It is possible to provide multiple possible API keys by specifying `DOCXTMPL_API_KEY_1`, `DOCXTMPL_API_KEY_2` and so on. |
| `DOCXTMPL_API_KEY_FILE` | *Not set* | If you want to use Docker secrets you can set `DOCXTMPL_API_KEY_FILE` instead of `DOCXTMPL_API_KEY`. If you specify both, both keys are accepted.<br />Similarly to above you can specify multiple files by using `DOCXTMPL_API_KEY_FILE_1`, `DOCXTMPL_API_KEY_FILE_2` and so on. |

The docker container contains some commonly used fonts.

## Using the Service

The `docxtmpl` service accepts Multipart `POST` requests containing exactly one `template` file and a `data` field containing a JSON object with the templating context. A request might look like this:

```http
POST / HTTP/1.1
Accept: application/pdf
Api-Key: <api-key>
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