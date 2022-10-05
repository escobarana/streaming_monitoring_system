FROM python:3.9

COPY . ./datasimulator

WORKDIR /datasimulator

# Update aptitude with new repo
RUN apt-get update

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -v -r requirements.txt

# Remove requirements file
RUN rm requirements.txt

# Run Flask App
CMD["flask", "--app", "flask_app.py", "-h", "0.0.0.0", "-p", "80"]