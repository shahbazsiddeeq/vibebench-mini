# Build from an official Python image and add Node 22
FROM python:3.11-slim

# Install Node 22 + git + build tools
RUN apt-get update && apt-get install -y curl git build-essential && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
 && apt-get install -y nodejs \
 && npm -v && node -v

# Workdir + copy
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY package.json package-lock.json* /app/
RUN npm ci || npm install

# Copy the rest
COPY . /app

# default command: run both tracks
CMD bash -lc "python runner/vibebench_runner.py --tasks tasks/python --out results.json --csv results.csv --metrics configs/metrics.v1.json \
 && node runner/vibebench_runner_js.mjs \
 && python scripts/analyze_results.py \
 && echo 'Done. Artifacts in /app (results.json, results.csv, scorecard.md, reports/, results_js.*)'"

 # Copy entrypoint
COPY scripts/docker_entrypoint.sh /usr/local/bin/vibebench
RUN chmod +x /usr/local/bin/vibebench

# Default entrypoint: runs the pipeline unless args are provided
ENTRYPOINT ["vibebench"]
# (no CMD → entrypoint handles default behavior)