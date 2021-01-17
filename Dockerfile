FROM python:3.8.7-alpine
WORKDIR /app
RUN apk add --no-cache ca-certificates apache2-utils
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD src src
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD [ "python", "-m", "src" ]