FROM httpd:latest


COPY httpd.conf /usr/local/apache2/bin/httpd
COPY httpd-vhosts.conf /usr/local/apache2/bin/httpd

#ENV http_proxy Module3.com -> 환경변수로 설정할 수 있나 찾아본 거에요. 뒤에는 Module3는 클라이언트가 접근하는 website명(임의로 정한거)
#ENV https_proxy Module3.com


#RUN mkdir -p /usr/local/apache2/conf/sites/

EXPOSE 80

CMD ["httpd", "-D", "FOREGROUNDED"]
#80/443
