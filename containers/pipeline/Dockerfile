FROM python:3.9.5

# set up location of code
WORKDIR /code
ENV PYTHONPATH=/code/scripts

# install cron
RUN apt-get update && apt-get install cron -y

# install python requirements
ADD ./containers/pipeline/requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

# copy repo
COPY ./ /code/

# Copy pull_defi_liquidity_info file to the cron.d directory
COPY /scheduler/pull_defi_liquidity_info /etc/cron.d/pull_defi_liquidity_info

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/pull_defi_liquidity_info

# Ensure there's a newline at the end of the cron file
RUN echo "" >> /etc/cron.d/pull_defi_liquidity_info

# Apply cron job
RUN crontab /etc/cron.d/pull_defi_liquidity_info

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run cron
CMD cron && tail -f /var/log/cron.log
