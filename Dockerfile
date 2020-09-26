FROM python:3.8.6-alpine
WORKDIR /app
ADD requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
ADD src src
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
CMD [ "python", "-m", "src" ]