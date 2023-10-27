FROM python:alpine

# Add LibreOffice and Packaged Fonts
RUN apk add --no-cache fontconfig font-carlito libreoffice openjdk17 \
    && fc-cache -f

# Add MS Fonts
RUN apk --no-cache add msttcorefonts-installer \
    && update-ms-fonts \
    && rm -rf /var/cache/* \
    && fc-cache -f

# Add More MS Fonts
RUN apk --no-cache add cabextract fontforge \
    && mkdir -p /usr/share/fonts/truetype/microsoft \
    && wget --no-verbose --show-progress --progress=bar:force:noscroll https://web.archive.org/web/20171225132744if_/https://download.microsoft.com/download/E/6/7/E675FFFC-2A6D-4AB0-B3EB-27C9F8C8F696/PowerPointViewer.exe \
    && cabextract --lowercase -F ppviewer.cab PowerPointViewer.exe \
    && cabextract --lowercase -F '*.ttf' -d /usr/share/fonts/truetype/microsoft ppviewer.cab \
    && cabextract --lowercase -F '*.ttc' -d . ppviewer.cab \
    && FONTFORGE_LANGUAGE=ff fontforge -c 'Open("cambria.ttc"); Generate("cambria.ttf")' \
    && FONTFORGE_LANGUAGE=ff fontforge -c 'Open("cambria.ttc(Cambria Math)"); Generate("cambria-math.ttf")' \
    && mv *.ttf /usr/share/fonts/truetype/microsoft \
    && rm *.ttc *.cab *.exe \
    && fc-cache -f

# Add Google Fonts
RUN mkdir -p /usr/share/fonts/truetype/google-fonts \
    && wget --no-verbose --show-progress --progress=bar:force:noscroll https://github.com/google/fonts/raw/main/ofl/caladea/Caladea-Bold.ttf -P /usr/share/fonts/truetype/google-fonts \
    && wget --no-verbose --show-progress --progress=bar:force:noscroll https://github.com/google/fonts/raw/main/ofl/caladea/Caladea-BoldItalic.ttf -P /usr/share/fonts/truetype/google-fonts \
    && wget --no-verbose --show-progress --progress=bar:force:noscroll https://github.com/google/fonts/raw/main/ofl/caladea/Caladea-Italic.ttf -P /usr/share/fonts/truetype/google-fonts \
    && wget --no-verbose --show-progress --progress=bar:force:noscroll https://github.com/google/fonts/raw/main/ofl/caladea/Caladea-Regular.ttf -P /usr/share/fonts/truetype/google-fonts \
    && fc-cache -f

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY requirements.txt ./
RUN adduser --disabled-password --uid 1000 templater \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

USER templater

COPY ./templater/ ./templater

EXPOSE 8000
CMD ["waitress-serve", "templater:app"]
