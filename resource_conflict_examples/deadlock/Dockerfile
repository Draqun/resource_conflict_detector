FROM ubuntu:latest

WORKDIR /root

COPY CMakeLists.txt .
COPY deadlock.cpp .
COPY helpers.cpp .
COPY helpers.hpp .
COPY run_application.sh .

RUN apt update
RUN apt -y install cmake gcc g++
RUN chmod +x run_application.sh
RUN cmake .
RUN make
RUN make clean


RUN echo "648000" > data.in

ENTRYPOINT bash -x run_application.sh