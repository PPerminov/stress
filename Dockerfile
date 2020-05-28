FROM ubuntu
WORKDIR /stress
RUN apt update && \
  apt install python3 stress coreutils -y && \
  apt clean && \
  rm -rf /var/cache/apt /var/lib/apt/lists/
COPY main.py .
COPY run.sh .
#COPY brute_force .
#COPY term.py .
CMD ./run.sh
ENV TYPE 2
