# Quotation Generator (Flask + WeasyPrint) — container image
# WeasyPrint needs Pango/Cairo/GDK-Pixbuf system libraries, so we install them here.
FROM python:3.12-slim

# System libraries required by WeasyPrint (PDF rendering) + fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libpangoft2-1.0-0 \
      libgdk-pixbuf-2.0-0 \
      libcairo2 \
      libffi8 \
      libjpeg62-turbo \
      shared-mime-info \
      fontconfig \
      fonts-dejavu-core \
      fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=5000

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

# Render/Railway inject $PORT. Bind gunicorn to it (single worker keeps memory
# low for the free 512 MB tier; long timeout for PDF generation).
CMD ["sh", "-c", "gunicorn app:app --bind 0.0.0.0:${PORT:-5000} --workers 1 --threads 2 --timeout 120"]
