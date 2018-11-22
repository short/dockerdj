FROM nginx:alpine

RUN apk update && apk upgrade && \
    apk add --no-cache bash git

RUN git clone https://github.com/short/test.git
RUN cd test
RUN cp -R /test/* /usr/share/nginx/html
# RUN rm /usr/share/nginx/html/index.html
RUN chown -R root:root /usr/share/nginx/html

# EXPOSE 80
