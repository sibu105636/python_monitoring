FROM python:2.7
WORKDIR /
#COPY /root/sitripa/scripts/script_scheduler.py /root/sitripa/quay_sanity/
#RUN pip install -r requirements.txt
#COPY . /root
ENV no_proxy=reg-dhc.app.corpintra.net
ADD docker /usr/bin/
ADD script_scheduler.py /
ADD daily_sanity.py /
ADD test1.sh /
ADD test2.sh /
ADD test3.sh /
ADD test4.sh /
COPY redis_prod.tar /root
#ADD config.json /root/.docker/
#COPY /root/sitripa/config.json /root
RUN pip install --proxy=http://53.81.3.37:3128  requests schedule diskcache prometheus_client
EXPOSE 9102
CMD ["python", "./script_scheduler.py"]
